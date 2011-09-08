from slumber import exceptions

SERIALIZERS = {
    "json": True,
    "yaml": True,
}

try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        SERIALIZERS["json"] = False

try:
    import yaml
except ImportError:
    SERIALIZERS["yaml"] = False

if not len([x for x in SERIALIZERS.values() if x]):
    raise exceptions.SerializerNoAvailable("There are no Available Serializers.")


class BaseSerializer(object):

    content_type = None

    def get_content_type(self):
        if self.content_type is None:
            raise NotImplementedError()
        return self.content_type

    def loads(self, data):
        raise NotImplementedError()

    def dumps(self, data):
        raise NotImplementedError()


class JsonSerializer(BaseSerializer):

    content_type = "application/json"

    def loads(self, data):
        return json.loads(data)

    def dumps(self, data):
        return json.dumps(data)


class YamlSerializer(BaseSerializer):

    content_type = "text/yaml"

    def loads(self, data):
        return yaml.safe_load(data)

    def dumps(self, data):
        return yaml.dump(data)


class Serializer(object):

    _serializers = {
        "json": JsonSerializer(),
        "yaml": YamlSerializer(),
    }

    def __init__(self, default_format="json"):
        default_format = default_format if default_format is not None else "json"

        self.available_serializers = [x[0] for x in SERIALIZERS.items() if x[1]]
        self.default_format = self.get_serializer(default_format)

    def get_serializer(self, name=None):
        if name is None:
            return self.default_format
        else:
            if not name in self.available_serializers:
                raise exceptions.SerializerNotAvailable("%s is not an available serializer" % name)
            return self._serializers[name]

    def loads(self, data, format=None):
        s = self.get_serializer(format)
        return s.loads(data)

    def dumps(self, data, format=None):
        s = self.get_serializer(format)
        return s.dumps(data)

    def get_content_type(self, format=None):
        s = self.get_serializer(format)
        return s.get_content_type()
