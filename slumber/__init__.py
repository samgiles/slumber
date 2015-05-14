import requests

try:
    from urllib.parse import urlparse, urlsplit, urlunsplit
except ImportError:
    from urlparse import urlparse, urlsplit, urlunsplit

from . import exceptions
from .serialize import Serializer
from .utils import url_join, iterator, copy_kwargs

__all__ = ["Resource", "API"]


class ResourceAttributesMixin(object):
    """
    A Mixin that allows access to an undefined attribute on a class.
    Instead of raising an attribute error, the undefined attribute will
    return a Resource Instance which can be used to make calls to the
    resource identified by the attribute.

    The type of the resource returned can be overridden by adding a
    resource_class attribute.

    It assumes that a Meta class exists at self._meta with all the required
    attributes.
    """

    def __getattr__(self, item):
        # Don't allow access to 'private' by convention attributes.
        # @@@: How would this work with resources names that begin with
        # underscores?
        if item.startswith("_"):
            raise AttributeError(item)

        kwargs = copy_kwargs(self._store)
        kwargs.update({"base_url": url_join(self._store["base_url"], item)})

        return self._get_resource(**kwargs)


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

        kwargs = copy_kwargs(self._store)

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

        return self._get_resource(**kwargs)

    def _request(self, method, data=None, files=None, params=None):
        serializer = self._store["serializer"]
        url = self.url()

        headers = {"accept": serializer.get_content_type()}

        if not files:
            headers["content-type"] = serializer.get_content_type()
            if data is not None:
                data = serializer.dumps(data)

        resp = self._store["session"].request(method, url, data=data, params=params, files=files, headers=headers)

        if 400 <= resp.status_code <= 499:
            exception_class = exceptions.HttpNotFoundError if resp.status_code == 404 else exceptions.HttpClientError
            raise exception_class("Client Error %s: %s" % (resp.status_code, url), response=resp, content=resp.content)
        elif 500 <= resp.status_code <= 599:
            raise exceptions.HttpServerError("Server Error %s: %s" % (resp.status_code, url), response=resp, content=resp.content)

        self._ = resp

        return resp

    def _handle_redirect(self, resp, **kwargs):
        # @@@ Hacky, see description in __call__
        resource_obj = self(url_override=resp.headers["location"])
        return resource_obj.get(**kwargs)

    def _try_to_serialize_response(self, resp):
        s = self._store["serializer"]
        if resp.status_code in [204, 205]:
            return

        if resp.headers.get("content-type", None) and resp.content:
            content_type = resp.headers.get("content-type").split(";")[0].strip()

            try:
                stype = s.get_serializer(content_type=content_type)
            except exceptions.SerializerNotAvailable:
                return resp.content

            if type(resp.content) == bytes:
                try:
                    encoding = requests.utils.guess_json_utf(resp.content)
                    return stype.loads(resp.content.decode(encoding))
                except:
                    return resp.content
            return stype.loads(resp.content)
        else:
            return resp.content

    def _process_response(self, resp):
        # TODO: something to expose headers and status

        if 200 <= resp.status_code <= 299:
            return self._try_to_serialize_response(resp)
        else:
            return  # @@@ We should probably do some sort of error here? (Is this even possible?)

    def url(self):
        url = self._store["base_url"]

        if self._store["append_slash"] and not url.endswith("/"):
            url = url + "/"

        return url

    # TODO: refactor these methods - lots of commonality
    def get(self, **kwargs):
        resp = self._request("GET", params=kwargs)
        return self._process_response(resp)

    def options(self, **kwargs):
        resp = self._request("OPTIONS", params=kwargs)
        return self._process_response(resp)

    def head(self, **kwargs):
        resp = self._request("HEAD", params=kwargs)
        return self._process_response(resp)

    def post(self, data=None, files=None, **kwargs):
        resp = self._request("POST", data=data, files=files, params=kwargs)
        return self._process_response(resp)

    def patch(self, data=None, files=None, **kwargs):
        resp = self._request("PATCH", data=data, files=files, params=kwargs)
        return self._process_response(resp)

    def put(self, data=None, files=None, **kwargs):
        resp = self._request("PUT", data=data, files=files, params=kwargs)
        return self._process_response(resp)

    def delete(self, **kwargs):
        resp = self._request("DELETE", params=kwargs)
        if 200 <= resp.status_code <= 299:
            if resp.status_code == 204:
                return True
            else:
                return True  # @@@ Should this really be True?
        else:
            return False

    def _get_resource(self, **kwargs):
        return self.__class__(**kwargs)


class API(ResourceAttributesMixin, object):

    resource_class = Resource

    def __init__(self, base_url=None, auth=None, format=None, append_slash=True, session=None, serializer=None):
        if serializer is None:
            serializer = Serializer(default=format)

        if session is None:
            session = requests.session()

        if auth is not None:
            session.auth = auth

        self._store = {
            "base_url": base_url,
            "format": format if format is not None else "json",
            "append_slash": append_slash,
            "session": session,
            "serializer": serializer,
        }

        # Do some Checks for Required Values
        if self._store.get("base_url") is None:
            raise exceptions.ImproperlyConfigured("base_url is required")

    def _get_resource(self, **kwargs):
        return self.resource_class(**kwargs)
