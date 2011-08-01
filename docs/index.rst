Slumber documentation
=====================

Slumber is a python library that provides a convenient yet powerful object
orientated interface to ReSTful APIs. It acts as a wrapper around the
excellent httplib2_ library and abstracts away the handling of urls, serialization,
and processing requests.

.. _httplib2: http://code.google.com/p/httplib2/

.. toctree::
   :maxdepth: 2

   tutorial
   options

Getting Help
============

There are two primary ways of getting help. We have a `mailing list`_ hosted at
Google (http://groups.google.com/group/python-slumber/) and an IRC channel
(`#slumber on irc.freenode.net`_) to get help, want to bounce idea or
generally shoot the breeze.

.. _`mailing list`: http://groups.google.com/group/python-slumber/
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

Slumber requires the following modules. If you use Pip_, you can install
the necessary bits via the included ``requirements.txt``:

* Python 2.5+
* httplib2
* simplejson (If using Python 2.5, or you desire the speedups for JSON serialization)
* pyyaml (If you are using the optional yaml serialization)

.. _Pip: http://pip.openplans.org/

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`