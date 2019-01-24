ARG IMAGE
FROM $IMAGE
WORKDIR /tox
WORKDIR /app
COPY . .
RUN pip install --upgrade pip tox --requirement requirements-dev.txt
CMD tox -e "$(tox --listenvs-all | grep "$PYTHON_VERSION-" | tr '\n' ',')"
