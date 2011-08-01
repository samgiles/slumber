import httplib2


class HttpClient(httplib2.Http):

    def get(self, *args, **kwargs):
        kwargs.update({
            "method": "GET",
        })
        return self.request(*args, **kwargs)
