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

.. code-block:: python

    from mbq import metrics

    metrics.init(namespace='my-service', constant_tags={'env': ENV_NAME})

    metrics.increment('metric.name', 5, tags={'something': 'awesome'})

    # show the rest

HTTP Metrics with Django Middleware
-----------------------------------
This library also contains a piece of Django middleware you can use to create an awesome `HTTP Datadog dashboard <https://app.datadoghq.com/dash/893352>`_ for your service! The middleware reports the following metrics to Datadog:

* Request duration in milliseconds
* Status codes (200, 404, 503 etc)
* Status ranges (2xx, 4xx, 5xx, etc)
* Response content length
* Request path

Adding the middleware to your Django project and configuring the Datadog dashboard is quick and easy:

1. Install ``mbq.metrics >= 0.2.1`` in your service (If you are already using the mbq.metrics middleware, upgrading to 0.2.1 will change the metric names being sent to datadog)
2. Include ``mbq.metrics.contrib.django.middleware.timing.TimingMiddleware`` in the ``MIDDLEWARE`` constant in your ``settings.py`` file.
3. Go to the `Invoicing HTTP Datadog dashboard <https://app.datadoghq.com/dash/893352>`_. Click the gear in the top right and then “Clone Dashboard”.
4. Name the new dashboard ``Yourservicename: HTTP``
5. For each graph in your new dashboard, click edit, and change the metric from ``invoicing.response`` to ``Yourservicename.response``

Tada!

HTTP Metrics with WSGI Middleware (Flask)
-----------------------------------------

Middleware is also included that can be easily plugged into a Flask app to generate the same sort of metrics referenced in the Django section above. Requires mbq.metrics >= 0.3.0.

See `the implementation in Isengard <https://github.com/managedbyq/isengard/pull/51/files>`_ for an example.

Testing
-------

We now use `tox` for local testing across multiple python environments. Before this use `pyenv` to install the following python interpreters: cpython{2.7, 3.5, 3.6} and pypy3

install and run tox:

.. code-block:: bash
    $ pip install tox
    $ tox
    $
    $ # run a specific environment
    $ tox -e py36-django111
    $

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
