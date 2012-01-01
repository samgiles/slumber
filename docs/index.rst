Slumber documentation
=====================

Slumber is a python library that provides a convenient yet powerful object
orientated interface to ReSTful APIs. It acts as a wrapper around the
excellent requests_ library and abstracts away the handling of urls, serialization,
and processing requests.

.. _requests: http://python-requests.org/

.. toctree::
   :maxdepth: 2

   tutorial
   options
   howitworks

Getting Help
============

There are two primary ways of getting help. I have an IRC channel
(`#slumber on irc.freenode.net`_) to get help, want to bounce idea or
generally shoot the breeze.

.. _#slumber on irc.freenode.net: irc://irc.freenode.net/slumber

QuickStart
==========

1. Install Slumber::

    $ pip install slumber

2. Install Optional Requirements::

    pip install simplejson pyyaml

3. Use Slumber!

Requirements
============

Slumber requires the following modules:

* Python 2.5+
* requests
* simplejson (If using Python 2.5, or you desire the speedups for JSON serialization)
* pyyaml (If you are using the optional yaml serialization)

.. _Pip: http://pip.openplans.org/

Testing Slumber requires the following modules:

* Mock

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
