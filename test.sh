#!/usr/bin/env bash
pip install --upgrade pip tox tox-venv tox-travis
tox -e "$(tox --listenvs-all | grep "$PYTHON_VERSION-" | tr '\n' ',')"
