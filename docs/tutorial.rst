.. _ref-tutorial:

============================
Getting Started with Slumber
============================

Installation
============

Slumber is available on PyPi and the preferred method of install is
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
    >>> ## Connect to http://slumber.in/api/v1/ with the Basic Auth user/password of demo/demo
    >>> api = slumber.API("http://slumber.in/api/v1/", auth=("demo", "demo")
    >>> ## GET http://slumber.in/api/v1/note/
    >>> ##     Note: Any kwargs passed to get(), post(), put(), delete() will be used as url parameters
    >>> api.note.get()
    >>> ## POST http://slumber.in/api/v1/note/
    >>> new = api.note.post({"title": "My Test Note", "content": "This is the content of my Test Note!"})
    >>> ## PUT http://slumber.in/api/v1/note/{id}/
    >>> api.note(new["id"]).put({"content": "I just changed the content of my Test Note!"})
    >>> ## GET http://slumber.in/api/v1/note/{id}/
    >>> api.note(new["id"]).get()
    >>> ## DELETE http://slumber.in/api/v1/note/{id}/
    >>> api.note(new["id"]).delete()

Url Parameters
==============

Passing an url parameter to Slumber is easy. If you wanted to say, use Tastypie's ApiKey
authentication, you could do so like::

    >>> api.resource.get(username="example", api_key="1639eb74e86717f410c640d2712557aac0e989c8")

If you wanted to filter the Slumber demo api for notes that start with Bacon, you could do::

    >>> import slumber
    >>> api = slumber.API("http://slumber.in/api/v1/", auth=("demo", "demo"))
    >>> ## GET http://slumber.in/api/v1/note/?title__startswith=Bacon
    >>> api.note.get(title__startswith="Bacon")


Nested Resources
================

Nested resources are also easy and works just how a single level resource works::

    >>> ## GET /resource1/resource2/
    >>> api.resource1.resource2.get()

    >>> ## GET /resource1/1/resource2/
    >>> api.resource1(1).resource2.get()
