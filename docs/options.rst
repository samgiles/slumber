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

With Tastypie ApikeyAuthentication you can use::

    from requests.auth import AuthBase
    
    class TastypieApikeyAuth(AuthBase):
        def __init__(self, username, apikey):
            self.username = username
            self.apikey = apikey

        def __call__(self, r):
            r.headers['Authorization'] = "ApiKey {0}:{1}".format(self.username, self.apikey)
            return r

    api = slumber.API("http://path/to/my/api/", auth=TastypieApikeyAuth("myuser", "mypass"))

To Use Digest or OAuth please consult the requests documentation. The auth
argument is passed directly to requests and thus works exactly the same way
and accepts exactly the same arguments.

File uploads
============

You may upload files by supplying a dictionary in the form {'key': file-like-object} as the value of the
``files`` parameter in ``post``, ``patch`` or ``put`` calls.  E.g.::

    with open('/home/philip/out.txt') as fp:
        api.file.post({'name': 'my file'}, files={'file': fp}) 

Will do a POST to ``/api/file/`` with a multipart-form-data request.


Serializer
==========

Slumber allows you to use any serialization you want. It comes with json and
yaml but creating your own is easy. By default it will attempt to use json. You
can change the default by specifying a ``format`` argument to your api class.::

    # Use Yaml instead of Json
    api = slumber.API("http://path/to/my/api/", format="yaml")

If you want to override the serializer for a particular request, you can do that as well::

    # Use Yaml instead of Json for just this request.
    api = slumber.API("http://path/to/my/api/") # Serializer defaults to Json
    api.resource_name(format="yaml").get() # Serializer will be Yaml

If you want to create your own serializer you can do so. A serialize inherits from
``slumber.serialize.BaseSerializer`` and implements ``loads``, ``dumps``. It
also must have a class member of ``key`` which will be the string key for this
serialization (such as "json").The final requirement is either a class member
of ``content_type`` which is the content type to use for requests (such as
"application/json") or define a ``get_content_type`` method.

An example::

    class PickleSerializer(slumber.serialize.BaseSerializer):
        key = "pickle"
        content_type = "x-application/pickle"

        def loads(self, data):
            return pickle.loads(data)

        def dumps(self, data):
            return pickle.dumps(data)

Once you have a custom serializer you can pass it to slumber like so::

    from slumber import serialize
    import slumber

    s = serialize.Serializer(
                    default="pickle",
                    serializers=[
                        serialize.JsonSerializer(),
                        serialize.YamlSerializer(),
                        PickleSerializer(),
                    ]
                )
    api = slumber.API("http://example.com/api/v1/", format="pickle", serializer=s)

Slashes
=======

Slumber assumes by default that all urls should end with a slash. If you do not
want this behavior you can control it via the append_slash option which can be
set by passing append_slash to the ``slumber.API`` kwargs.
