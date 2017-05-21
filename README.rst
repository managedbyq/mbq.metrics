mbq.metrics: metrics for the masses
===================================

.. image:: https://travis-ci.org/managedbyq/mbq.metrics.svg?branch=master
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

    metrics.increment('metric.name', 5, tags={'something': 'awesome')

    # show the rest

API Reference
-------------


Contributing
------------
