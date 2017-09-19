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

FAQs
----

**Where do I put the DogStatsd agent configuration?**

You don't! ``mbq.metrics`` is pre-baked with assumptions about how Q runs it's services. Specifically, we assume that each service runs in a Docker container and that that container is running on a VM that's running the DogStatsD agent. In that way we can automatically configure our client to reach outside of the container and easily push metrics to the agent. 
Read more in the `datadogpy documentation <http://datadogpy.readthedocs.io/en/latest/index.html#datadog.initialize>`_ or `in the source <https://github.com/DataDog/datadogpy/blob/fd6646a6e8cde1d7a8c2f6e324d04e8d7f8a6f8c/datadog/dogstatsd/route.py#L15>`_.

API Reference
-------------


Contributing
------------
