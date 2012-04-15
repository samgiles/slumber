import posixpath
import urlparse

import requests

from slumber import exceptions
from slumber.serialize import Serializer

__all__ = ["Resource", "API"]


def url_join(base, *args):
    """
    Helper function to join an arbitrary number of url segments together.
    """
    scheme, netloc, path, query, fragment = urlparse.urlsplit(base)
    path = path if len(path) else "/"
    path = posixpath.join(path, *[('%s' % x) for x in args])
    return urlparse.urlunsplit([scheme, netloc, path, query, fragment])


class ResourceAttributesMixin(object):
    """
    A Mixin that makes it so that accessing an undefined attribute on a class
    results in returning a Resource Instance. This Instance can then be used
    to make calls to the a Resource.

    It assumes that a Meta class exists at self._meta with all the required
    attributes.
    """

    def __getattr__(self, item):
        if item.startswith("_"):
            raise AttributeError(item)

        kwargs = {}
        for key, value in self._store.iteritems():
            kwargs[key] = value

        kwargs.update({"base_url": url_join(self._store["base_url"], item)})

        return Resource(**kwargs)


class Resource(ResourceAttributesMixin, object):
    """
    Resource provides the main functionality behind slumber. It handles the
    attribute -> url, kwarg -> query param, and other related behind the scenes
    python to HTTP transformations. It's goal is to represent a single resource
    which may or may not have children.

    It assumes that a Meta class exists at self._meta with all the required
    attributes.
    """

    def __init__(self, *args, **kwargs):
        self._store = kwargs

    def __call__(self, id=None, format=None, url_override=None):
        """
        Returns a new instance of self modified by one or more of the available
        parameters. These allows us to do things like override format for a
        specific request, and enables the api.resource(ID).get() syntax to get
        a specific resource by it's ID.
        """

        # Short Circuit out if the call is empty
        if id is None and format is None and url_override is None:
            return self

        kwargs = {}
        for key, value in self._store.iteritems():
            kwargs[key] = value

        if id is not None:
            kwargs["base_url"] = url_join(self._store["base_url"], id)

        if format is not None:
            kwargs["format"] = format

        if url_override is not None:
            # @@@ This is hacky and we should probably figure out a better way
            #    of handling the case when a POST/PUT doesn't return an object
            #    but a Location to an object that we need to GET.
            kwargs["base_url"] = url_override

        kwargs["session"] = self._store["session"]

        return self.__class__(**kwargs)

    def get_serializer(self):
        return Serializer(default_format=self._store["format"])

    def _request(self, method, data=None, params=None):
        s = self.get_serializer()
        url = self._store["base_url"]

        if self._store["append_slash"] and not url.endswith("/"):
            url = url + "/"

        resp = self._store["session"].request(method, url, data=data, params=params, headers={"content-type": s.get_content_type(), "accept": s.get_content_type()})

        if 400 <= resp.status_code <= 499:
            raise exceptions.HttpClientError("Client Error %s: %s" % (resp.status_code, url), response=resp, content=resp.content)
        elif 500 <= resp.status_code <= 599:
            raise exceptions.HttpServerError("Server Error %s: %s" % (resp.status_code, url), response=resp, content=resp.content)

        return resp

    def get(self, **kwargs):
        s = self.get_serializer()

        resp = self._request("GET", params=kwargs)
        if 200 <= resp.status_code <= 299:
            if resp.status_code == 200:
                return s.loads(resp.content)
            else:
                return resp.content
        else:
            return  # @@@ We should probably do some sort of error here? (Is this even possible?)

    def post(self, data, **kwargs):
        s = self.get_serializer()

        resp = self._request("POST", data=s.dumps(data), params=kwargs)
        if 200 <= resp.status_code <= 299:
            if resp.status_code == 201:
                # @@@ Hacky, see description in __call__
                resource_obj = self(url_override=resp.headers["location"])
                return resource_obj.get(params=kwargs)
            else:
                return resp.content
        else:
            # @@@ Need to be Some sort of Error Here or Something
            return

    def put(self, data, **kwargs):
        s = self.get_serializer()

        resp = self._request("PUT", data=s.dumps(data), params=kwargs)
        if 200 <= resp.status_code <= 299:
            if resp.status_code == 204:
                return True
            else:
                return True  # @@@ Should this really be True?
        else:
            return False

    def delete(self, **kwargs):
        resp = self._request("DELETE", params=kwargs)
        if 200 <= resp.status_code <= 299:
            if resp.status_code == 204:
                return True
            else:
                return True  # @@@ Should this really be True?
        else:
            return False


class API(ResourceAttributesMixin, object):

    def __init__(self, base_url=None, auth=None, format=None, append_slash=True, session=None):
        self._store = {
            "base_url": base_url,
            "format": format if format is not None else "json",
            "append_slash": append_slash,
            "session": requests.session(auth=auth) if session is None else session,
        }

        # Do some Checks for Required Values
        if self._store.get("base_url") is None:
            raise exceptions.ImproperlyConfigured("base_url is required")
