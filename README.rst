mbq.metrics: metrics for the masses
===================================

.. image:: https://img.shields.io/pypi/v/mbq.metrics.svg
    :target: https://pypi.python.org/pypi/mbq.metrics

.. image:: https://img.shields.io/pypi/l/mbq.metrics.svg
    :target: https://pypi.python.org/pypi/mbq.metrics

.. image:: https://img.shields.io/pypi/pyversions/mbq.metrics.svg
    :target: https://pypi.python.org/pypi/mbq.metrics

.. image:: https://img.shields.io/travis/managedbyq/mbq.metrics/master.svg
    :target: https://travis-ci.org/managedbyq/mbq.metrics

Installation
------------

.. code-block:: bash

    $ pip install mbq.metrics
    🚀✨

Guaranteed fresh.


Getting started
---------------
Initialize mbq.metrics in your ``settings.py`` like this:

.. code-block:: python

    from mbq import env, metrics

    ENV = env.get_environment("ENV_NAME")
    SERVICE_NAME = 'service-name'
    metrics.init(SERVICE_NAME, ENV, constant_tags={'env': ENV_NAME})

HTTP Metrics with Django Middleware
-----------------------------------
This library also contains a piece of Django middleware you can use to create an awesome `HTTP Datadog dashboard <https://app.datadoghq.com/dash/893352>`_ for your service! The middleware reports the following metrics to Datadog:

* Request duration in milliseconds
* Status codes (200, 404, 503 etc)
* Status ranges (2xx, 4xx, 5xx, etc)
* Response content length
* Request path

Adding the middleware to your Django project and configuring the Datadog dashboard is quick and easy: just include ``mbq.metrics.contrib.django.middleware.timing.TimingMiddleware`` in the ``MIDDLEWARE`` constant in your ``settings.py`` file.

Tada!

HTTP Metrics with WSGI Middleware (Flask)
-----------------------------------------

Middleware is also included that can be easily plugged into a Flask app to generate the same sort of metrics referenced in the Django section above. Requires mbq.metrics >= 0.3.0.

See `the implementation in Isengard <https://github.com/managedbyq/isengard/pull/51/files>`_ for an example.

Testing
-------

Tests are automatically in `Travis CI <https://travis-ci.org/managedbyq/mbq.metrics>`_ but you can also run tests locally using `docker-compose`.
We now use `tox` for local testing across multiple python environments. Before this use `pyenv` to install the following python interpreters: cpython{2.7, 3.5, 3.6} and pypy3

install and run tox:

.. code-block:: bash

    $ docker-compose build py36
    Building py36
    Step 1/5 : ARG IMAGE
    Step 2/5 : FROM $IMAGE
     ---> 60cd00be8967
    Step 3/5 : WORKDIR /tox
     ---> Running in f55aee265e33
    Removing intermediate container f55aee265e33
     ---> 2b31757df863
    Step 4/5 : WORKDIR /app
     ---> Running in a1bc5e661ca3
    Removing intermediate container a1bc5e661ca3
     ---> 6f1f17a29a8e
    Step 5/5 : COPY . .
     ---> 55eef13da5e6
    Successfully built 55eef13da5e6
    Successfully tagged mbqmetrics_py36:latest
    $ docker-compose up py36
    Recreating mbqmetrics_py36_1 ... done
    Attaching to mbqmetrics_py36_1
    py36_1   | Requirement already up-to-date: pip in /usr/local/lib/python3.6/site-packages (18.0)
    py36_1   | Collecting tox
    py36_1   |   Downloading https://files.pythonhosted.org/packages/df/53/13660f04ef09ece4aefcce6b8f79c1586fc34dee1cbedd7c153e02f93489/tox-3.2.1-py2.py3-none-any.whl (62kB)
    py36_1   | Collecting tox-venv
    py36_1   |   Downloading https://files.pythonhosted.org/packages/bd/bd/f981a5bcd5b90b65fbfd3e6d6d93d592721e2e946eaa08e9ea5d325a4077/tox_venv-0.3.1-py2.py3-none-any.whl
    py36_1   | Collecting tox-travis
    py36_1   |   Downloading https://files.pythonhosted.org/packages/a0/f0/55a0d561161ceac9da512d221547cd0405f0cbf5dfba7352cd36d7bfdace/tox_travis-0.10-py2.py3-none-any.whl
    py36_1   | Collecting py<2,>=1.4.17 (from tox)
    py36_1   |   Downloading https://files.pythonhosted.org/packages/c8/47/d179b80ab1dc1bfd46a0c87e391be47e6c7ef5831a9c138c5c49d1756288/py-1.6.0-py2.py3-none-any.whl (83kB)
    py36_1   | Collecting six<2,>=1.0.0 (from tox)
    py36_1   |   Downloading https://files.pythonhosted.org/packages/67/4b/141a581104b1f6397bfa78ac9d43d8ad29a7ca43ea90a2d863fe3056e86a/six-1.11.0-py2.py3-none-any.whl
    py36_1   | Requirement already satisfied, skipping upgrade: setuptools>=30.0.0 in /usr/local/lib/python3.6/site-packages (from tox) (40.0.0)
    py36_1   | Collecting pluggy<1,>=0.3.0 (from tox)
    py36_1   |   Downloading https://files.pythonhosted.org/packages/f5/f1/5a93c118663896d83f7bcbfb7f657ce1d0c0d617e6b4a443a53abcc658ca/pluggy-0.7.1-py2.py3-none-any.whl
    py36_1   | Collecting virtualenv>=1.11.2 (from tox)
    py36_1   |   Downloading https://files.pythonhosted.org/packages/b6/30/96a02b2287098b23b875bc8c2f58071c35d2efe84f747b64d523721dc2b5/virtualenv-16.0.0-py2.py3-none-any.whl (1.9MB)
    py36_1   | Installing collected packages: py, six, pluggy, virtualenv, tox, tox-venv, tox-travis
    py36_1   | Successfully installed pluggy-0.7.1 py-1.6.0 six-1.11.0 tox-3.2.1 tox-travis-0.10 tox-venv-0.3.1 virtualenv-16.0.0
    py36_1   | GLOB sdist-make: /app/setup.py
    py36_1   | py36-django111 create: /tox/py36-django111
    py36_1   | py36-django111 installdeps: ., Django>=1.11,<2.0
    py36_1   | py36-django111 inst: /tox/dist/mbq.metrics-0.4.0.zip
    py36_1   | py36-django111 installed: You are using pip version 10.0.1, however version 18.0 is available.,You should consider upgrading via the 'pip install --upgrade pip' command.,certifi==2018.8.24,chardet==3.0.4,datadog==0.22.0,decorator==4.3.0,Django==1.11.15,idna==2.7,mbq.metrics==0.4.0,pytz==2018.5,requests==2.19.1,simplejson==3.16.0,urllib3==1.23
    py36_1   | py36-django111 runtests: PYTHONHASHSEED='2612051782'
    py36_1   | py36-django111 runtests: commands[0] | python -Wall -m unittest discover tests
    py36_1   | /tox/py36-django111/lib/python3.6/site-packages/datadog/dogstatsd/base.py:306: DeprecationWarning: invalid escape sequence \:
    py36_1   |   return string.replace('\n', '\\n').replace('m:', 'm\:')
    py36_1   | ................
    py36_1   | ----------------------------------------------------------------------
    py36_1   | Ran 16 tests in 0.094s
    py36_1   |
    py36_1   | OK
    # ...snip...


Shipping a New Release
----------------------

1. Bump the version in `setup.py`
2. Go to `Releases` in GitHub and "Draft a New Release"
3. After creating a new release, Travis CI will pick up the new release and ship it to PyPi

FAQs
----

**Where do I put the DogStatsd agent configuration?**

You don't! ``mbq.metrics`` is pre-baked with assumptions about how Q runs it's services. Specifically, we assume that each service runs in a Docker container and that that container is running on a VM that's running the DogStatsD agent. In that way we can automatically configure our client to reach outside of the container and easily push metrics to the agent.
Read more in the `datadogpy documentation <http://datadogpy.readthedocs.io/en/latest/index.html#datadog.initialize>`_ or `in the source <https://github.com/DataDog/datadogpy/blob/fd6646a6e8cde1d7a8c2f6e324d04e8d7f8a6f8c/datadog/dogstatsd/route.py#L15>`_.

API Reference
-------------


Contributing
------------
