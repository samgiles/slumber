from slumber import exceptions

_SERIALIZERS = {
    "json": True,
    "yaml": True,
}

try:
    import json
except ImportError:
    _SERIALIZERS["json"] = False

try:
    import yaml
except ImportError:
    _SERIALIZERS["yaml"] = False


class BaseSerializer(object):

    content_types = None
    key = None

    def get_content_type(self):
        if self.content_types is None:
            raise NotImplementedError()
        return self.content_types[0]

    def loads(self, data):
        raise NotImplementedError()

    def dumps(self, data):
        raise NotImplementedError()


class JsonSerializer(BaseSerializer):

    content_types = [
                        "application/json",
                        "application/x-javascript",
                        "text/javascript",
                        "text/x-javascript",
                        "text/x-json",
                    ]
    key = "json"

    def loads(self, data):
        return json.loads(data)

    def dumps(self, data):
        return json.dumps(data)


class YamlSerializer(BaseSerializer):

    content_types = ["text/yaml"]
    key = "yaml"

    def loads(self, data):
        return yaml.safe_load(str(data))

    def dumps(self, data):
        return yaml.dump(data)


class Serializer(object):

    def __init__(self, default=None, serializers=None):
        if default is None:
            default = "json" if _SERIALIZERS["json"] else "yaml"

        if serializers is None:
            serializers = [x() for x in [JsonSerializer, YamlSerializer] if _SERIALIZERS[x.key]]

        if not serializers:
            raise exceptions.SerializerNoAvailable("There are no Available Serializers.")

        self.serializers = {}

        for serializer in serializers:
            self.serializers[serializer.key] = serializer

        self.default = default

    def get_serializer(self, name=None, content_type=None):
        if name is None and content_type is None:
            return self.serializers[self.default]
        elif name is not None and content_type is None:
            if not name in self.serializers:
                raise exceptions.SerializerNotAvailable("%s is not an available serializer" % name)
            return self.serializers[name]
        else:
            for x in self.serializers.values():
                for ctype in x.content_types:
                    if content_type == ctype:
                        return x
            raise exceptions.SerializerNotAvailable("%s is not an available serializer" % content_type)

    def loads(self, data, format=None):
        s = self.get_serializer(format)
        return s.loads(data)

    def dumps(self, data, format=None):
        s = self.get_serializer(format)
        return s.dumps(data)

    def get_content_type(self, format=None):
        s = self.get_serializer(format)
        return s.get_content_type()
