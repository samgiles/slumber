__version__ = "dev"

__author__ = "Donald Stufft"
__email__ = "donald.stufft@gmail.com"

__description__ = "A library that makes consuming a ReST API easier and more convenient"
__url__ = "https://github.com/dstufft/slumber/"

__all__ = ["Resource", "API"]

import copy
# @@@ Should we look for one with speedups?
# @@@ Python 2.5 Compatibility?
import json
import urllib
import urlparse

from slumber import exceptions
from slumber.http import HttpClient

class Resource(object):

    def __init__(self, domain, endpoint=None):
        self.domain = domain
        self.endpoint = endpoint

        self.http_client = HttpClient()

    def __call__(self, id):
        obj = copy.deepcopy(self)
        obj.object_id = id
        return obj

    def _request(self, method, **kwargs):
        if kwargs.has_key("url"):
            url = kwargs.pop("url")
        else:
            url = urlparse.urljoin(self.domain, self.endpoint)

            if hasattr(self, "object_id"):
                url = urlparse.urljoin(url, str(self.object_id))

            if not url.endswith("/"):
                url += "/"

        if kwargs.has_key("body"):
            body = kwargs.pop("body")
        else:
            body = None

        if kwargs:
            url = "?".join([url, urllib.urlencode(kwargs)])

        resp, content = self.http_client.request(url, method, body=body, headers={"content-type": "application/json"})

        if 400 <= resp.status <= 499:
            raise exceptions.SlumberHttpClientError("Client Error %s: %s" % (resp.status, url), response=resp, content=content)
        elif 500 <= resp.status <= 599:
            raise exceptions.SlumberHttpServerError("Server Error %s: %s" % (resp.status, url), response=resp, content=content)

        return resp, content
    
    def get(self, **kwargs):
        resp, content = self._request("GET", **kwargs)
        if 200 <= resp.status <= 299:
            if resp.status == 200:
                return json.loads(content)
            else:
                return content
        else:
            return # @@@ We should probably do some sort of error here? (Is this even possible?)

    def post(self, data, **kwargs):
        kwargs.update({
            "body": json.dumps(data)
        })
        resp, content = self._request("POST", **kwargs)
        if 200 <= resp.status <= 299:
            if resp.status == 201:
                return self.get(url=resp.location)
            else:
                return content
        else:
            # @@@ Need to be Some sort of Error Here or Something
            return

    def put(self, data, **kwargs):
        kwargs.update({
            "body": json.dumps(data)
        })
        resp, content = self._request("PUT", **kwargs)
        if 200 <= resp.status <= 299:
            if resp.status == 204:
                return True
            else:
                return True # @@@ Should this really be True?
        else:
            return False

    def delete(self, **kwargs):
        resp, content = self._request("DELETE", **kwargs)
        if 200 <= resp.status <= 299:
            if resp.status == 204:
                return True
            else:
                return True # @@@ Should this really be True?
        else:
            return False


class APIMeta(object):

    resources = {}
    http = {
        "schema": "http",
        "hostname": None,
        "port": "80",
        "path": "/",

        "params": "",
        "query": "",
        "fragment": "",
    }

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            default_value = getattr(self, key)
            
            if isinstance(default_value, dict) and isinstance(value, dict):
                setattr(self, key, default_value.update(value))
            else:
                setattr(self, key, value)

    @property
    def base_url(self):
        ORDERING = ["schema", "hostname", "port", "path", "params", "query", "fragment"]
        urlparts = []
        for key in ORDERING:
            if key in ["path"]:
                urlparts.append("")
            else:
                urlparts.append(self.http[key])
        return urlparse.urlunparse(urlparts[:1] + [":".join([str(x) for x in urlparts[1:3]])] + urlparts[3:])

    @property
    def api_url(self):
        ORDERING = ["schema", "hostname", "port", "path", "params", "query", "fragment"]
        urlparts = []
        for key in ORDERING:
            urlparts.append(self.http[key])
        return urlparse.urlunparse(urlparts[:1] + [":".join([str(x) for x in urlparts[1:3]])] + urlparts[3:])


class API(object):

    class Meta:
        pass

    def __init__(self, api_url=None, discover_resources=False):
        class_meta = getattr(self, "Meta", None)
        if class_meta is not None:
            keys = [x for x in dir(class_meta) if not x.startswith("_")]
            meta_dict = dict([(x, getattr(class_meta, x)) for x in keys])
        else:
            meta_dict = {}

        self._meta = APIMeta(**meta_dict)

        if api_url is not None:
            # Attempt to parse the url into it's parts
            parsed = urlparse.urlparse(api_url)
            for key in self._meta.http.keys():
                val = getattr(parsed, key, None)
                if val:
                    self._meta.http[key] = val

        self.http_client = HttpClient()

        if discover_resources:
            self.discover_resources()

    def __getattr__(self, item):
        try:
            return self._meta.resources[item]
        except KeyError:
            self._meta.resources[item] = Resource(self._meta.base_url, endpoint=urlparse.urljoin(self._meta.http["path"], item))
            return self._meta.resources[item]

    def discover_resources(self):
        resp, content = self.http_client.get(self._meta.api_url)

        resources = json.loads(content)
        for name, resource in resources.iteritems():
            kwargs = {
                "domain": self._meta.base_url,
                "endpoint": resource.get("list_endpoint", self._meta.http["path"] + name + "/")
            }
            self._meta.resources[name] = Resource(**kwargs)