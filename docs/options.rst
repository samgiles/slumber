=======
Options
=======

Slumber comes with only a couple options.

Authentication
==============

Out of the box Slumber should support any authentication method supported
by httplib2. These include Basic, Digest, WSSE, HMAC Digest and Google Account
Authentication. However only Basic and Digest get tested currently.

Specify Authentication
----------------------

Specifying authentication credentials is easy. When you create your slumber
api instance, instead of doing::

    api = slumber.API("http://path/to/my/api/")

You supply the username and password like::

    api = slumber.API("http://path/to/my/api/", authentication={"name": "myuser", "password": "mypass"})

And slumber will attempt to use those credentials anytime it's told it is not authorized.

Serializer
==========

Slumber allows you to use either json or yaml as your serializer. It defaults to using
json. You can change this default by specifying a ``default_format`` argument to your
api class.::

    # Use Yaml instead of Json
    api = slumber.API("http://path/to/my/api/", default_format="yaml")

If you want to override the serializer for a particular request, you can do that as well::

    # Use Yaml instead of Json for just this request.
    api = slumber.API("http://path/to/my/api/") # Serializer defaults to Json
    api.resource_name.get(format="yaml") # Serializer will be Yaml
