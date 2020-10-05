# stdlib
import pathlib

# 3rd party
from pytest_regressions.file_regression import FileRegressionFixture


def check_file_regression(data, file_regression: FileRegressionFixture, extension=".txt"):
	file_regression.check(data, encoding="UTF-8", extension=extension)


def check_file_output(filename: pathlib.Path, file_regression: FileRegressionFixture):
	data = filename.read_text(encoding="UTF-8")
	extension = filename.suffix
	if extension == ".py":
		extension = "._py_"
	check_file_regression(data, file_regression, extension)
