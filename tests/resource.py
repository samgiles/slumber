import mock
import unittest
import httplib2
import slumber


class ResourceAttributesMixinTestCase(unittest.TestCase):

    def test_attribute_fallback_to_resource(self):
        class ResourceMixinTest(slumber.ResourceAttributesMixin, slumber.MetaMixin, object):
            class Meta:
                authentication = None
                base_url = None
                format = "json"

        rmt = ResourceMixinTest(base_url="http://example.com/")
        self.assertTrue(isinstance(rmt.example, slumber.Resource))


class ResourceTestCase(unittest.TestCase):

    def setUp(self):
        self.base_resource = slumber.Resource(base_url="http://example/api/v1/test")

    def test_get_serializer(self):
        self.assertTrue(isinstance(self.base_resource.get_serializer(), slumber.Serializer))

    def test_request_200(self):
        # Mock a Response Object
        r = mock.Mock(spec=httplib2.Response)
        r.status = 200

        # Mock The httplib2.Http class
        self.base_resource._http = mock.Mock(spec=httplib2.Http)
        self.base_resource._http.request.return_value = (r, "Mocked Content")

        resp, content = self.base_resource._request("GET")

        self.assertTrue(resp is r)
        self.assertEqual(content, "Mocked Content")

        self.base_resource._http.request.assert_called_once_with(
            "http://example/api/v1/test",
            "GET",
            body=None,
            headers={"content-type": self.base_resource.get_serializer().get_content_type()}
        )
