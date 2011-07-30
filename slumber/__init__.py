__version__ = "dev"

__author__ = "Donald Stufft"
__email__ = "donald.stufft@gmail.com"

__description__ = "A library that makes consuming a ReST API easier and more convenient"
__url__ = "https://github.com/dstufft/slumber/"

__all__ = ["Resource", "API"]

import httplib2
import json # @@@ Should we look for one with speedups?

class Resource(object):

    def __init__(self, domain, list_endpoint=None, schema=None):
        self.domain = domain
        self.endpoints = {}
        self.schema = None

        if list_endpoint is not None:
            self.endpoints["list"] = list_endpoint
        if schema is not None:
            self.endpoints["schema"] = schema


class API(object):

    def __init__(self, base_url):
        self.base_url = base_url if base_url.endswith("/") else "%s/" % base_url
        self._resources = {}
        self.discover_resources()

    def discover_resources(self):
        h = httplib2.Http()
        resp, content = h.request(self.base_url)

        resources = json.loads(content)
        for name, resource in resources.iteritems():
            kwargs = dict(
                [x for x in resource.items() if x[0] in ["list_endpoint", "schema"]]
            )
            self._resources[name] = Resource(**kwargs)