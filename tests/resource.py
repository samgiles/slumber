import mock
import unittest
import requests
import slumber


class ResourceTestCase(unittest.TestCase):

    def setUp(self):
        self.base_resource = slumber.Resource(base_url="http://example/api/v1/test", format="json", append_slash=False)

    def test_get_serializer(self):
        self.assertTrue(isinstance(self.base_resource.get_serializer(), slumber.Serializer))

    def test_request_200(self):
        r = mock.Mock(spec=requests.Response)
        r.status_code = 200
        r.content = "Mocked Content"

        self.base_resource._store.update({
            "session": mock.Mock(spec=requests.Session),
        })
        self.base_resource._store["session"].request.return_value = r

        resp = self.base_resource._request("GET")

        self.assertTrue(resp is r)
        self.assertEqual(resp.content, "Mocked Content")

        self.base_resource._store["session"].request.assert_called_once_with(
            "GET",
            "http://example/api/v1/test",
            data=None,
            params=None,
            headers={"content-type": self.base_resource.get_serializer().get_content_type(), "accept": self.base_resource.get_serializer().get_content_type()}
        )
