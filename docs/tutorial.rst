.. _ref-tutorial:

============================
Getting Started with Slumber
============================

Installation
============

Slumber is available on PyPi and the preffered method of install is
using Pip.

1. Install Slumber::

    $ pip install slumber

2. Install Optional Dependencies

   **[OPTIONAL]** PyYaml *(Required for the yaml serializer)*::

       $ pip install pyyaml

   **[OPTIONAL]** SimpleJson *(Required for the json serializer on Python2.5, or for speedups)*::

       $ pip install simplejson

Using
=====

Using Slumber is easy. Using an example ReST API made with `django-tastypie`_
which you can see at http://slumber.in/api/v1/.

.. _django-tastypie: http://github.com/toastdriven/django-tastypie/

.. code-block:: pycon

    >>> import slumber
    >>> api = slumber.API("http://slumber.in/api/v1/", authentication={"name": "demo", "password": "demo"})
    >>> ## GET http://slumber.in/api/v1/note/
    >>> api.note.get()
    >>> ## POST http://slumber.in/api/v1/note/
    >>> new = api.note.post({"title": "My Test Note", "content": "This is the content of my Test Note!"})
    >>> ## PUT http://slumber.in/api/v1/note/{id}/
    >>> api.note(new["id"]).put({"content": "I just changed the content of my Test Note!"})
    >>> ## GET http://slumber.in/api/v1/note/{id}/
    >>> api.note(new["id"]).get()
    >>> ## DELETE http://slumber.in/api/v1/note/{id}/
    >>> api.note(new["id"]).delete()