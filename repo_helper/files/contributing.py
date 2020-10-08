#!/usr/bin/env python
#
#  contributing.py
"""
Contributing information for GitHub and documentation, plus GitHub issue templates.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import pathlib
import re
from typing import List

# 3rd party
import jinja2
from domdf_python_tools.paths import PathPlus

# this package
from repo_helper.files import management

__all__ = ["make_contributing", "make_docs_contributing", "make_issue_templates"]


def github_bash_block(*commands: str) -> str:
	"""
	Formats the given commands in a reStructuredText bash
	code block suitable for rendering on GitHub.

	:param commands:
	"""

	if not commands:
		return ''

	buf = f".. code-block:: bash"
	buf += "\n\n"

	for command in commands:
		if re.match(r"^ ?[>$] ?", command):
			buf += f"	{command.lstrip()}\n"
		else:
			buf += f"	$ {command}\n"

	return buf


def sphinx_bash_block(*commands):
	# TODO: fix from above
	if not commands:
		return ''

	buf = f".. prompt:: bash"
	buf += "\n\n"

	for command in commands:
		buf += f"	{command}\n"

	return buf


@management.register("contributing")
def make_contributing(repo_path: pathlib.Path, templates: jinja2.Environment) -> List[str]:
	"""
	Add CONTRIBUTING.rst to the desired repo

	:param repo_path: Path to the repository root.
	:param templates:
	:type templates: jinja2.Environment
	"""

	contributing = templates.get_template("CONTRIBUTING.rst")

	PathPlus(repo_path / "CONTRIBUTING.rst").write_clean(contributing.render(bash_block=github_bash_block))

	if (repo_path / "CONTRIBUTING.md").is_file():
		(repo_path / "CONTRIBUTING.md").unlink()

	return ["CONTRIBUTING.rst", "CONTRIBUTING.md"]


@management.register("contributing", ["enable_docs"])
def make_docs_contributing(repo_path: pathlib.Path, templates: jinja2.Environment) -> List[str]:
	"""
	Add CONTRIBUTING.rst to the documentation directory of the repo

	:param repo_path: Path to the repository root.
	:param templates:
	:type templates: jinja2.Environment
	"""

	contributing = templates.get_template("CONTRIBUTING.rst")
	content = "\n".join(["Overview", "---------"]
						+ contributing.render(bash_block=sphinx_bash_block).splitlines()[3:])

	docs_dir = PathPlus(repo_path / templates.globals["docs_dir"])
	docs_dir.maybe_make(parents=True)
	contributing_rst = (docs_dir / "contributing.rst")
	contributing_rst.write_clean(content)

	return [str(contributing_rst.relative_to(repo_path))]


@management.register("issue_templates")
def make_issue_templates(repo_path: pathlib.Path, templates: jinja2.Environment) -> List[str]:
	"""
	Add issue templates for GitHub to the desired repo

	:param repo_path: Path to the repository root.
	:param templates:
	:type templates: jinja2.Environment
	"""

	managed_files = []

	issue_template_dir = PathPlus(repo_path / ".github" / "ISSUE_TEMPLATE")
	issue_template_dir.maybe_make(parents=True)

	for filename in ["bug_report.md", "feature_request.md"]:
		filepath = issue_template_dir / filename
		filepath.write_clean(templates.get_template(filename).render())
		managed_files.append(str(filepath.relative_to(repo_path)))

	return managed_files