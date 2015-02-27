import unittest
import slumber
import slumber.serialize


class ResourceTestCase(unittest.TestCase):
    def setUp(self):
        self.data = {
            "foo": "bar",
        }

    def test_json_get_serializer(self):
        s = slumber.serialize.Serializer()

        serializer = None
        for content_type in [
            "application/json",
            "application/x-javascript",
            "text/javascript",
            "text/x-javascript",
            "text/x-json",
        ]:
            serializer = s.get_serializer(content_type=content_type)
            self.assertEqual(type(serializer), slumber.serialize.JsonSerializer,
                             "content_type %s should produce a JsonSerializer")

        result = serializer.dumps(self.data)
        self.assertEqual(result, '{"foo": "bar"}')
        self.assertEqual(self.data, serializer.loads(result))

    def test_yaml_get_serializer(self):
        s = slumber.serialize.Serializer()

        serializer = None
        for content_type in [
            "text/yaml",
        ]:
            serializer = s.get_serializer(content_type=content_type)
            self.assertEqual(type(serializer), slumber.serialize.YamlSerializer,
                             "content_type %s should produce a YamlSerializer")

        result = serializer.dumps(self.data)
        self.assertEqual(result, "{foo: bar}\n")
        self.assertEqual(self.data, serializer.loads(result))
