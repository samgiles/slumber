import copy
import urllib
import urlparse

from slumber import exceptions
from slumber.http import HttpClient
from slumber.serialize import Serializer

__all__ = ["Resource", "API"]


class Meta(object):
    """
    Model that acts as a container class for a meta attributes for a larger
    class. It stuffs any kwarg it gets in it's init as an attribute of itself.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)


class MetaMixin(object):
    """
    Mixin that provides the Meta class support to add settings to instances
    of slumber objects. Meta settings cannot start with a _.
    """

    def __init__(self, *args, **kwargs):
        # Get a List of all the Classes we in our MRO, find any attribute named
        #     Meta on them, and then merge them together in order of MRO
        metas = reversed([x.Meta for x in self.__class__.mro() if hasattr(x, "Meta")])
        final_meta = {}

        # Merge the Meta classes into one dict
        for meta in metas:
            final_meta.update(dict([x for x in meta.__dict__.items() if not x[0].startswith("_")]))

        # Update the final Meta with any kwargs passed in
        for key in final_meta.keys():
            if key in kwargs:
                final_meta[key] = kwargs.pop(key)

        self._meta = Meta(**final_meta)

        # Finally Pass anything unused along the MRO
        super(MetaMixin, self).__init__(*args, **kwargs)


class Resource(object):

    def __init__(self, base_url, format="json", authentication=None):
        self.base_url = base_url
        self.authentication = authentication
        self.format = format

        self.http_client = HttpClient()

        if self.authentication is not None:
            self.http_client.add_credentials(**self.authentication)

    def __call__(self, id=None, format=None, url_override=None):
        if id is not None or format is not None or url_override is not None:
            obj = copy.deepcopy(self)
            if id is not None:
                obj.object_id = id
            if format is not None:
                obj.format = format
            if url_override is not None:
                # @@@ This is hacky. Should probably Figure out a Better Way
                #       can't just pass it to get/post/put/delete because
                #       it'll override the kwarg -> url paramter.
                obj.url_override = url_override
            return obj
        return self

    def get_serializer(self):
        try:
            return self._serializer
        except AttributeError:
            self._serializer = Serializer(default_format=self.format)
            return self._serializer

    def _request(self, method, **kwargs):
        s = self.get_serializer()

        if hasattr(self, "url_override"):
            url = self.url_override
        else:
            url = self.base_url

            if hasattr(self, "object_id"):
                url = urlparse.urljoin(url, str(self.object_id))

        if "body" in kwargs:
            body = kwargs.pop("body")
        else:
            body = None

        if kwargs:
            url = "?".join([url, urllib.urlencode(kwargs)])

        resp, content = self.http_client.request(url, method, body=body, headers={"content-type": s.get_content_type()})

        if 400 <= resp.status <= 499:
            raise exceptions.SlumberHttpClientError("Client Error %s: %s" % (resp.status, url), response=resp, content=content)
        elif 500 <= resp.status <= 599:
            raise exceptions.SlumberHttpServerError("Server Error %s: %s" % (resp.status, url), response=resp, content=content)

        return resp, content

    def get(self, **kwargs):
        s = self.get_serializer()

        resp, content = self._request("GET", **kwargs)
        if 200 <= resp.status <= 299:
            if resp.status == 200:
                return s.loads(content)
            else:
                return content
        else:
            return  # @@@ We should probably do some sort of error here? (Is this even possible?)

    def post(self, data, **kwargs):
        s = self.get_serializer()

        resp, content = self._request("POST", body=s.dumps(data), **kwargs)
        if 200 <= resp.status <= 299:
            if resp.status == 201:
                # @@@ Hacky, see description in __call__
                resource_obj = self(url_override=resp["location"])
                return resource_obj.get(**kwargs)
            else:
                return content
        else:
            # @@@ Need to be Some sort of Error Here or Something
            return

    def put(self, data, **kwargs):
        s = self.get_serializer()

        resp, content = self._request("PUT", body=s.dumps(data), **kwargs)
        if 200 <= resp.status <= 299:
            if resp.status == 204:
                return True
            else:
                return True  # @@@ Should this really be True?
        else:
            return False

    def delete(self, **kwargs):
        resp, content = self._request("DELETE", **kwargs)
        if 200 <= resp.status <= 299:
            if resp.status == 204:
                return True
            else:
                return True  # @@@ Should this really be True?
        else:
            return False


class API(MetaMixin, object):

    class Meta:
        resources = {}

        default_format = "json"
        authentication = None

        base_url = None

    def __init__(self, base_url, **kwargs):
        super(API, self).__init__(base_url=base_url, **kwargs)

        self.http_client = HttpClient()

        if self._meta.authentication is not None:
            self.http_client.add_credentials(**self._meta.authentication)

    def __getattr__(self, item):
        try:
            return self._meta.resources[item]
        except KeyError:
            self._meta.resources[item] = Resource(
                urlparse.urljoin(self._meta.base_url, item),
                format=self._meta.default_format,
                authentication=self._meta.authentication
            )
            return self._meta.resources[item]
