How Slumber Works Behind the Scenes
===================================

Behind the scenes slumber is really 2 things. It is a translator from python code
into urls, and it is a serializer/deserializer helper.

Python to Url Translation
-------------------------

The url translation portion of slumber is fairly simple but powerful. It is
basically a list of url fragments that get joined together.

In the call::

    >>> api.note.get()

Slumber translates this by adding the url value for ``api`` (say http://slumber.in/api/v1/)
with the url value for note. The url value for an attribute is equal to it's name, so
in this case slumber essentially does ``"http://slumber.in/api/v1/" + "note"``,

The same holds true when you pass in an ID to a resource. It just adds another
segment to the url list.

This means that in this call::

    >>> api.note(1).get()

Slumber translates it to::

    >>> "http://slumber.in/api/v1/" + "note" + "/" + str(1)

Nested Resources follow the same principle.

The other part of an url that Slumber translates is keyword arguments (kwargs) to ``get()``, ``post()``,
``put()``, ``delete()`` into query string params. This again is a fairly simple
operation which then gets added to the end of the url.

There are also helpful utiltity methods such as ``url()`` which return the
final string representation of a resource.

The Final portion of Slumber's Python to HTTP is that the first arg passed to
each of the HTTP functions is serialized, and then passed into the HTTP request
as the body of the request.

(De)Serialization
-----------------

Slumber also has a built in Serialization framework. This is a fairly simple wrapper
around (simple)json and/or pyyaml that controls setting the correct content-type
on a request, and will automatically serialize or deserialize any incoming or outgoing
request body.
