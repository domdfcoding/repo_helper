#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  yaml_parser.py
"""
Parse configuration values from a ``YAML`` file.
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
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import json
import pathlib
from typing import Any, Dict, Iterable, List, Type, Union

# this package
from git_helper import configuration
import git_helper

# this package
import importlib_resources  # type: ignore
import yaml

from git_helper.configuration import *
from git_helper.config_vars import make_schema, parse_extras, ConfigVar
from ytools import validate  # type: ignore  # TODO


__all__ = [
		"parse_yaml",
		"get_tox_python_versions",
		]


def parse_yaml(repo_path: pathlib.Path):
	"""
	Parse configuration values from a ``YAML`` file.

	:param repo_path: Path to the repository root.
	:type repo_path: pathlib.Path

	:return:
	:rtype: dict
	"""

	with importlib_resources.path(git_helper, "git_helper_schema.json") as schema:
		validate(str(schema), [repo_path / "git_helper.yml"])

	config_vars = {}

	# load user settings from git_helper.yml
	with (repo_path / "git_helper.yml").open() as file:
		# The FullLoader parameter handles the conversion from YAML
		#   scalar values to Python the dictionary format
		raw_config_vars = yaml.load(file, Loader=yaml.FullLoader)

	# --------------------------------------

	metadata_vars: List[Type[ConfigVar]] = [
			# Metadata
			author,
			email,
			username,
			modname,
			version,
			copyright_years,
			repo_name,
			pypi_name,
			import_name,
			classifiers,
			keywords,
			license,
			short_desc,
			source_dir,

			# Optional Features
			enable_tests,
			enable_releases,
			docker_shields,
			docker_name,

			# Packaging
			manifest_additional,
			py_modules,
			console_scripts,
			setup_pre,
			additional_setup_args,
			platforms,

			# Documentation
			rtfd_author,
			preserve_custom_theme,
			sphinx_html_theme,
			extra_sphinx_extensions,
			intersphinx_mapping,
			sphinx_conf_preamble,
			sphinx_conf_epilogue,
			html_theme_options,
			html_context,
			enable_docs,
			docs_dir,

			# Other
			imgbot_ignore,
			]

	for var in metadata_vars:
		config_vars[var.__name__] = var.get(raw_config_vars)

	# Packaging
	extras_require, additional_requirements_files = parse_extras(raw_config_vars, repo_path)
	config_vars["extras_require"] = extras_require
	config_vars["additional_requirements_files"] = additional_requirements_files

	# Python Versions
	config_vars["python_deploy_version"] = python_deploy_version.get(raw_config_vars)
	config_vars["python_versions"] = python_versions.get(raw_config_vars)
	config_vars["min_py_version"] = min(config_vars["python_versions"])

	# Tox
	tox_py_versions = get_tox_python_versions(config_vars["python_versions"])
	config_vars["tox_py_versions"] = tox_py_versions
	for var_name in {
			"tox_requirements",
			"tox_build_requirements",
			}:
		config_vars[var_name] = raw_config_vars.get(var_name, [])
	config_vars["tox_testenv_extras"] = raw_config_vars.get("tox_testenv_extras", "")

	# Travis
	tox_travis_versions = get_tox_travis_python_versions(config_vars["python_versions"], tox_py_versions)
	gh_actions_versions = get_gh_actions_python_versions(config_vars["python_versions"], tox_py_versions)
	tox_travis_versions[config_vars["python_deploy_version"]] += ", mypy"
	config_vars["tox_travis_versions"] = tox_travis_versions
	config_vars["gh_actions_versions"] = gh_actions_versions

	travis_vars: List[Type[ConfigVar]] = [
			travis_site,
			travis_pypi_secure,
			travis_extra_install_pre,
			travis_extra_install_post,
			travis_additional_requirements,
			travis_ubuntu_version,
			]

	for var in travis_vars:
		config_vars[var.__name__] = var.get(raw_config_vars)

	other_vars: List[Type[ConfigVar]] = [
			# Conda & Anaconda
			enable_conda,
			conda_channels,
			conda_description,

			# Other
			tests_dir,
			additional_ignore,
			exclude_files,
			pkginfo_extra,
			]

	for var in other_vars:
		config_vars[var.__name__] = var.get(raw_config_vars)

	# config_vars["lint_fix_list"] = lint_fix_list
	# config_vars["lint_belligerent_list"] = lint_belligerent_list
	# config_vars["lint_warn_list"] = lint_warn_list

	def add_classifier(classifier):
		if classifier not in config_vars["classifiers"]:
			config_vars["classifiers"].append(classifier)

	if (repo_path / config_vars["import_name"].replace(".", "/") / "py.typed").is_file():
		add_classifier("Typing :: Typed")

	return config_vars


def get_tox_python_versions(python_versions: Iterable[str]) -> List[str]:
	"""

	:param python_versions:

	:return:
	"""

	tox_py_versions = []

	for py_version in python_versions:
		py_version = str(py_version).replace(".", '')
		if not py_version.startswith("py"):
			py_version = f"py{py_version}"
		tox_py_versions.append(py_version)

	return tox_py_versions


def get_tox_travis_python_versions(
		python_versions: Iterable[str],
		tox_py_versions: Iterable[str],
		) -> Dict[str, str]:
	"""

	:param python_versions:
	:param tox_py_versions:

	:return:
	"""

	tox_travis_matrix: Dict[str, str] = {}

	for py_version, tox_py_version in zip(python_versions, tox_py_versions):
		tox_travis_matrix[str(py_version)] = str(tox_py_version)

	return tox_travis_matrix


def get_gh_actions_python_versions(
		python_versions: Iterable[str],
		tox_py_versions: Iterable[str],
		) -> Dict[str, str]:
	"""

	:param python_versions:
	:param tox_py_versions:

	:return:
	"""

	tox_travis_matrix: Dict[str, str] = {}

	for py_version, tox_py_version in zip(python_versions, tox_py_versions):
		if tox_py_version != "docs":
			tox_travis_matrix[str(py_version)] = str(tox_py_version)

	return tox_travis_matrix


def dump_schema() -> Dict[str, Any]:
	"""

	:return:
	:rtype: str
	"""
	# from genson import SchemaBuilder
	# builder = SchemaBuilder()
	# builder.add_schema(schema)

	schema = make_schema(*[getattr(configuration, x) for x in configuration.__all__])

	with importlib_resources.path(git_helper, "git_helper_schema.json") as schema_file:
		pathlib.Path(schema_file).write_text(json.dumps(schema, indent=2))

	return schema


if __name__ == "__main__":
	schema = dump_schema()
	print(json.dumps(schema, indent=2))
