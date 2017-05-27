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

API Reference
-------------


Contributing
------------
