#  This file is managed by 'repo_helper'. Don't edit it directly.
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This file is distributed under the same license terms as the program it came with.
#  There will probably be a file called LICEN[S/C]E in the same directory as this file.
#
#  In any case, this program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# This script based on https://github.com/rocky/python-uncompyle6/blob/master/__pkginfo__.py
#

# stdlib
import pathlib

__all__ = [
		"__copyright__",
		"__version__",
		"repo_root",
		"install_requires",
		"extras_require",
		]

__copyright__ = """
2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
"""

__version__ = "2021.1.27"

repo_root = pathlib.Path(__file__).parent
install_requires = (repo_root / "requirements.txt").read_text(encoding="utf-8").split('\n')
extras_require = {
		"testing": [
				"pytest>=6.0.0",
				"domdf-python-tools[testing]>=1.6.0",
				"twine>=3.2.0",
				"check_wheel_contents>=0.2.0"
				],
		"all": [
				"check_wheel_contents>=0.2.0",
				"domdf-python-tools[testing]>=1.6.0",
				"pytest>=6.0.0",
				"twine>=3.2.0"
				]
		}
