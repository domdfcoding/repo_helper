#!/usr/bin/env python
#
#  test_ci_cd.py
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

# 3rd party
import pytest
from pytest_regressions.file_regression import FileRegressionFixture  # type: ignore

# this package
from repo_helper.files.ci_cd import (
		ensure_bumpversion,
		make_github_ci,
		make_github_docs_test,
		make_github_manylinux,
		make_github_octocheese,
		make_make_conda_recipe,
		make_travis,
		make_travis_deploy_conda,
		remove_copy_pypi_2_github
		)
from tests.common import check_file_output


def test_travis_case_1(tmpdir, demo_environment, file_regression: FileRegressionFixture):
	tmpdir_p = pathlib.Path(tmpdir)

	managed_files = make_travis(tmpdir_p, demo_environment)
	assert managed_files == [".travis.yml"]
	check_file_output(tmpdir_p / managed_files[0], file_regression)


def test_travis_case_2(tmpdir, demo_environment, file_regression):
	tmpdir_p = pathlib.Path(tmpdir)

	demo_environment.globals.update(
			dict(
					travis_ubuntu_version="bionic",
					travis_extra_install_pre=["sudo apt update"],
					travis_extra_install_post=["sudo apt install python3-gi"],
					travis_additional_requirements=["isort", "black"],
					enable_tests=False,
					enable_conda=False,
					enable_releases=False,
					)
			)

	managed_files = make_travis(tmpdir_p, demo_environment)
	assert managed_files == [".travis.yml"]
	check_file_output(tmpdir_p / managed_files[0], file_regression)

	# # Reset
	# demo_environment.globals.update(dict(
	# 		enable_tests=True,
	# 		enable_conda=True,
	# 		enable_releases=True,
	# 		))
	return


@pytest.mark.parametrize("pure_python", [True, False])
@pytest.mark.parametrize("enable_conda", [True, False])
@pytest.mark.parametrize("enable_tests", [True, False])
@pytest.mark.parametrize("enable_releases", [True, False])
def test_travis_case_3(
		tmpdir,
		demo_environment,
		file_regression,
		pure_python,
		enable_conda,
		enable_tests,
		enable_releases,
		):
	tmpdir_p = pathlib.Path(tmpdir)

	demo_environment.globals.update(
			dict(
					pure_python=pure_python,
					enable_tests=enable_conda,
					enable_conda=enable_tests,
					enable_releases=enable_releases,
					)
			)

	managed_files = make_travis(tmpdir_p, demo_environment)
	assert managed_files == [".travis.yml"]
	check_file_output(tmpdir_p / managed_files[0], file_regression)
	return


def test_travis_deploy_conda(tmpdir, demo_environment, file_regression: FileRegressionFixture):
	tmpdir_p = pathlib.Path(tmpdir)

	managed_files = make_travis_deploy_conda(tmpdir_p, demo_environment)
	assert managed_files == [".ci/travis_deploy_conda.sh"]
	check_file_output(tmpdir_p / managed_files[0], file_regression)


def test_github_ci_case_1(tmpdir, demo_environment, file_regression: FileRegressionFixture):
	tmpdir_p = pathlib.Path(tmpdir)

	managed_files = make_github_ci(tmpdir_p, demo_environment)
	assert managed_files == [".github/workflows/python_ci.yml", ".github/workflows/python_ci_macos.yml"]
	assert (tmpdir_p / managed_files[0]).is_file()
	assert not (tmpdir_p / managed_files[1]).is_file()
	check_file_output(tmpdir_p / managed_files[0], file_regression)


def test_github_ci_case_2(tmpdir, demo_environment, file_regression: FileRegressionFixture):
	tmpdir_p = pathlib.Path(tmpdir)

	demo_environment.globals.update(
			dict(
					travis_additional_requirements=["isort", "black"],
					platforms=["macOS"],
					)
			)

	managed_files = make_github_ci(tmpdir_p, demo_environment)
	assert managed_files == [".github/workflows/python_ci.yml", ".github/workflows/python_ci_macos.yml"]
	assert not (tmpdir_p / managed_files[0]).is_file()
	assert (tmpdir_p / managed_files[1]).is_file()
	check_file_output(tmpdir_p / managed_files[1], file_regression)


def test_github_ci_windows_38(tmpdir, demo_environment, file_regression: FileRegressionFixture):
	tmpdir_p = pathlib.Path(tmpdir)

	demo_environment.globals.update(
			dict(
					travis_additional_requirements=["isort", "black"],
					platforms=["macOS"],
					pure_python=False,
					)
			)

	demo_environment.globals["py_versions"] = ["3.6", "3.7", "3.8"]
	managed_files = make_github_ci(tmpdir_p, demo_environment)
	check_file_output(tmpdir_p / managed_files[1], file_regression)

	demo_environment.globals["py_versions"] = ["3.6", "3.7"]
	managed_files = make_github_ci(tmpdir_p, demo_environment)
	check_file_output(tmpdir_p / managed_files[1], file_regression)


def test_github_ci_case_3(tmp_pathplus, demo_environment):
	demo_environment.globals.update(dict(platforms=["Windows", "macOS"], ))

	managed_files = make_github_ci(tmp_pathplus, demo_environment)
	assert managed_files == [".github/workflows/python_ci.yml", ".github/workflows/python_ci_macos.yml"]
	assert (tmp_pathplus / managed_files[0]).is_file()
	assert (tmp_pathplus / managed_files[1]).is_file()

	# This time the files should be removed
	demo_environment.globals.update(dict(platforms=[], ))

	assert (tmp_pathplus / managed_files[0]).is_file()
	assert (tmp_pathplus / managed_files[1]).is_file()

	managed_files = make_github_ci(tmp_pathplus, demo_environment)
	assert managed_files == [".github/workflows/python_ci.yml", ".github/workflows/python_ci_macos.yml"]

	assert not (tmp_pathplus / managed_files[0]).is_file()
	assert not (tmp_pathplus / managed_files[1]).is_file()

	# # Reset
	# demo_environment.globals.update(
	# 		dict(
	# 				travis_additional_requirements=["isort", "black"],
	# 				platforms=["Windows", "macOS"],
	# 				)
	# 		)
	return


def test_remove_copy_pypi_2_github(tmp_pathplus, demo_environment):
	(tmp_pathplus / ".ci").mkdir()
	(tmp_pathplus / ".ci" / "copy_pypi_2_github.py").touch()
	assert (tmp_pathplus / ".ci" / "copy_pypi_2_github.py").is_file()

	assert remove_copy_pypi_2_github(tmp_pathplus, demo_environment) == [".ci/copy_pypi_2_github.py"]

	assert not (tmp_pathplus / ".ci" / "copy_pypi_2_github.py").is_file()


def test_make_make_conda_recipe(tmp_pathplus, demo_environment, file_regression):
	assert make_make_conda_recipe(tmp_pathplus, demo_environment) == ["make_conda_recipe.py"]
	check_file_output(tmp_pathplus / "make_conda_recipe.py", file_regression)


@pytest.mark.parametrize("py_versions", [["3.6", "3.7", "3.8"], ["3.6", "3.7"]])
@pytest.mark.parametrize("platforms", [["Linux"], ["Linux", "Windows"]])
def test_make_github_manylinux(
		tmp_pathplus,
		demo_environment,
		file_regression: FileRegressionFixture,
		platforms,
		py_versions,
		):

	demo_environment.globals["platforms"] = platforms
	demo_environment.globals["pure_python"] = False
	demo_environment.globals["py_versions"] = py_versions

	assert make_github_manylinux(tmp_pathplus, demo_environment) == [".github/workflows/manylinux_build.yml"]
	check_file_output(tmp_pathplus / ".github/workflows/manylinux_build.yml", file_regression)

	demo_environment.globals["platforms"] = ["Windows"]

	assert make_github_manylinux(tmp_pathplus, demo_environment) == [".github/workflows/manylinux_build.yml"]
	assert not (tmp_pathplus / ".github/workflows/manylinux_build.yml").is_file()


@pytest.mark.parametrize("platforms", [["Linux"], ["Linux", "Windows"]])
def test_make_github_manylinux_pure_python(
		tmp_pathplus,
		demo_environment,
		file_regression: FileRegressionFixture,
		platforms,
		):

	demo_environment.globals["platforms"] = platforms
	demo_environment.globals["pure_python"] = True

	assert make_github_manylinux(tmp_pathplus, demo_environment) == [".github/workflows/manylinux_build.yml"]
	assert not (tmp_pathplus / ".github/workflows/manylinux_build.yml").is_file()


def test_make_github_docs_test(tmp_pathplus, demo_environment, file_regression: FileRegressionFixture):
	assert make_github_docs_test(tmp_pathplus, demo_environment) == [".github/workflows/docs_test_action.yml"]
	check_file_output(tmp_pathplus / ".github/workflows/docs_test_action.yml", file_regression)


def test_make_github_octocheese(tmp_pathplus, demo_environment, file_regression: FileRegressionFixture):
	assert make_github_octocheese(tmp_pathplus, demo_environment) == [".github/workflows/octocheese.yml"]
	check_file_output(tmp_pathplus / ".github/workflows/octocheese.yml", file_regression)


@pytest.mark.parametrize("py_versions", [["3.6", "3.7", "3.8"], ["3.6", "3.7"]])
@pytest.mark.parametrize("enable_docs", [True, False])
def test_ensure_bumpversion(
		tmp_pathplus,
		demo_environment,
		file_regression: FileRegressionFixture,
		enable_docs,
		py_versions,
		):
	demo_environment.globals["version"] = "1.2.3"
	demo_environment.globals["enable_docs"] = enable_docs
	assert ensure_bumpversion(tmp_pathplus, demo_environment) == [".bumpversion.cfg"]
	check_file_output(tmp_pathplus / ".bumpversion.cfg", file_regression)


def test_ensure_bumpversion_remove_docs(tmp_pathplus, demo_environment, file_regression: FileRegressionFixture):
	demo_environment.globals["version"] = "1.2.3"

	demo_environment.globals["enable_docs"] = True
	ensure_bumpversion(tmp_pathplus, demo_environment)

	demo_environment.globals["enable_docs"] = False
	ensure_bumpversion(tmp_pathplus, demo_environment)

	check_file_output(tmp_pathplus / ".bumpversion.cfg", file_regression)