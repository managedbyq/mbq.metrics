#!/usr/bin/env bash
flake8 mbq/ tests/
tox -e "$(tox --listenvs-all | grep "$PYTHON_VERSION-" | tr '\n' ',')"
