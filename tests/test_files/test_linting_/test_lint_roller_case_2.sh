#!/bin/bash

# fix these
declare errors="E301,E303,E304,E305,E306,E502,W291,W293,W391,E226,E225,E241,E231,W292,E265,"

if [ -z "$(git status --porcelain --untracked-files=no)" ] || [ "$1" == "-f" ]; then
  # Working directory clean

  echo "Running autopep8"

  autopep8 --in-place --select "$errors" -a src/hello_world_cli.py

  autopep8 --in-place --select "$errors" -a --recursive testing/

  echo "Running flake8"

    >&2 flake8 src/hello_world_cli.py

    >&2 flake8 testing/

  exit 0

else
  # Uncommitted changes
  >&2 echo "git working directory is not clean"
  exit 1

fi
