=======
Options
=======

Slumber comes with only a couple options.

Authentication
==============

Out of the box Slumber should support any authentication method supported
by requests. These include Basic, Digest, OAuth. However only Basic and Digest
get tested currently.

Specify Authentication
----------------------

Specifying authentication credentials is easy. When you create your slumber
api instance, instead of doing::

    api = slumber.API("http://path/to/my/api/")

You supply the username and password (for Basic Auth) like::

    api = slumber.API("http://path/to/my/api/", auth=("myuser", "mypass"))

And slumber will attempt to use those credentials with each request.

To Use Digest or OAuth please consult the requests documentation. The auth
argument is passed directly to requests and thus works exactly the same way
and accepts exactly the same arguments.

Serializer
==========

Slumber allows you to use either json or yaml as your serializer. It defaults to using
json. You can change this default by specifying a ``format`` argument to your
api class.::

    # Use Yaml instead of Json
    api = slumber.API("http://path/to/my/api/", format="yaml")

If you want to override the serializer for a particular request, you can do that as well::

    # Use Yaml instead of Json for just this request.
    api = slumber.API("http://path/to/my/api/") # Serializer defaults to Json
    api.resource_name(format="yaml").get() # Serializer will be Yaml

Slashes
=======

Slumber assumes by default that all urls should end with a slash. If you do not
want this behavior you can control it via the append_slash option which can be
set by passing append_slash to the ``slumber.API`` kwargs.
