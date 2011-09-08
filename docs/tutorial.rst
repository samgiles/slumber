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

If you wanted to filter the Slumber demo api for notes that atart with Bacon, you could do::

    >>> import slumber
    >>> api = slumber.API("http://slumber.in/api/v1/", authentication={"name": "demo", "password": "demo"})
    >>> ## GET http://slumber.in/api/v1/note/?title__startswith=Bacon
    >>> api.note.get(title__startswith="Bacon")


Nested Resources
================

Nested resources are also easy and works just how a single level resource works::

    >>> ## GET /resource1/resource2/
    >>> api.resource1.resource2.get()

    >>> ## GET /resource1/1/resource2/
    >>> api.resource1(1).resource2.get()


Make your Own API Classes
=========================

In order to follow DRY Slumber allows you to create a special subclass of
``slumber.API`` that lets you specify default values. This looks like::

    >>> import slumber
    >>> class NoteApi(slumber.API):
    ...     class Meta:
    ...         base_url = "http://slumber.in/api/v1/"
    ...         authentication = {"name": "demo", "password": "demo"} # Can be From Settings
    ...         format = "json"
    ...
    >>> api = NoteApi()
    >>> ## GET http://slumber.in/api/v1/note/
    >>> api.note.get()

You can also override any of your subclasses Meta options by passing it to your
subclasses init method just as if you were using ``slumber.API`` directly. The only
required attribute is that you must either set a base_url in the Meta class, or 
you must pass it in through the init.

How Slumber's Meta System Works
-------------------------------

Slumber's Meta system works by gathering the paramters passed into the init method,
and gathering any Meta classes for any object in the classes MRO. It then merges
then together, letting init override classes, and subclasses overriding super classes.
