import mock
import unittest
import requests
import slumber
import slumber.serialize


class ResourceTestCase(unittest.TestCase):

    def setUp(self):
        self.base_resource = slumber.Resource(base_url="http://example/api/v1/test", format="json", append_slash=False)

    def test_get_200_json(self):
        r = mock.Mock(spec=requests.Response)
        r.status_code = 200
        r.headers = {"content-type": "application/json"}
        r.content = '{"result": ["a", "b", "c"]}'

        self.base_resource._store.update({
            "session": mock.Mock(spec=requests.Session),
            "serializer": slumber.serialize.Serializer(),
        })
        self.base_resource._store["session"].request.return_value = r

        resp = self.base_resource._request("GET")

        self.assertTrue(resp is r)
        self.assertEqual(resp.content, r.content)

        self.base_resource._store["session"].request.assert_called_once_with(
            "GET",
            "http://example/api/v1/test",
            data=None,
            params=None,
            headers={"content-type": self.base_resource._store["serializer"].get_content_type(), "accept": self.base_resource._store["serializer"].get_content_type()}
        )

        resp = self.base_resource.get()
        self.assertEqual(resp['result'], ['a', 'b', 'c'])

    def test_get_200_text(self):
        r = mock.Mock(spec=requests.Response)
        r.status_code = 200
        r.headers = {"content-type": "text/text"}
        r.content = "Mocked Content"

        self.base_resource._store.update({
            "session": mock.Mock(spec=requests.Session),
            "serializer": slumber.serialize.Serializer(),
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
            headers={"content-type": self.base_resource._store["serializer"].get_content_type(), "accept": self.base_resource._store["serializer"].get_content_type()}
        )

        resp = self.base_resource.get()
        self.assertEqual(resp, r.content)

    def test_post_201_redirect(self):
        r1 = mock.Mock(spec=requests.Response)
        r1.status_code = 201
        r1.headers = {"location": "http://example/api/v1/test/1"}
        r1.content = ''

        r2 = mock.Mock(spec=requests.Response)
        r2.status_code = 200
        r2.headers = {}
        r2.content = '{"result": ["a", "b", "c"]}'

        self.base_resource._store.update({
            "session": mock.Mock(spec=requests.Session),
            "serializer": slumber.serialize.Serializer(),
        })
        self.base_resource._store["session"].request.side_effect = (r1, r2)

        resp = self.base_resource._request("POST")

        self.assertTrue(resp is r1)
        self.assertEqual(resp.content, r1.content)

        self.base_resource._store["session"].request.assert_called_once_with(
            "POST",
            "http://example/api/v1/test",
            data=None,
            params=None,
            headers={"content-type": self.base_resource._store["serializer"].get_content_type(), "accept": self.base_resource._store["serializer"].get_content_type()}
        )

        resp = self.base_resource.post(data={'foo': 'bar'})
        self.assertEqual(resp['result'], ['a', 'b', 'c'])

    def test_post_decodable_response(self):
        r = mock.Mock(spec=requests.Response)
        r.status_code = 200
        r.content = '{"result": ["a", "b", "c"]}'
        r.headers = {}

        self.base_resource._store.update({
            "session": mock.Mock(spec=requests.Session),
            "serializer": slumber.serialize.Serializer(),
        })
        self.base_resource._store["session"].request.return_value = r

        resp = self.base_resource._request("POST")

        self.assertTrue(resp is r)
        self.assertEqual(resp.content, r.content)

        self.base_resource._store["session"].request.assert_called_once_with(
            "POST",
            "http://example/api/v1/test",
            data=None,
            params=None,
            headers={"content-type": self.base_resource._store["serializer"].get_content_type(), "accept": self.base_resource._store["serializer"].get_content_type()}
        )

        resp = self.base_resource.post(data={'foo': 'bar'})
        self.assertEqual(resp['result'], ['a', 'b', 'c'])

    def test_patch_201_redirect(self):
        r1 = mock.Mock(spec=requests.Response)
        r1.status_code = 201
        r1.headers = {"location": "http://example/api/v1/test/1"}
        r1.content = ''

        r2 = mock.Mock(spec=requests.Response)
        r2.status_code = 200
        r2.headers = {}
        r2.content = '{"result": ["a", "b", "c"]}'

        self.base_resource._store.update({
            "session": mock.Mock(spec=requests.Session),
            "serializer": slumber.serialize.Serializer(),
        })
        self.base_resource._store["session"].request.side_effect = (r1, r2)

        resp = self.base_resource._request("PATCH")

        self.assertTrue(resp is r1)
        self.assertEqual(resp.content, r1.content)

        self.base_resource._store["session"].request.assert_called_once_with(
            "PATCH",
            "http://example/api/v1/test",
            data=None,
            params=None,
            headers={"content-type": self.base_resource._store["serializer"].get_content_type(), "accept": self.base_resource._store["serializer"].get_content_type()}
        )

        resp = self.base_resource.patch(data={'foo': 'bar'})
        self.assertEqual(resp['result'], ['a', 'b', 'c'])

    def test_patch_decodable_response(self):
        r = mock.Mock(spec=requests.Response)
        r.status_code = 200
        r.content = '{"result": ["a", "b", "c"]}'
        r.headers = {}

        self.base_resource._store.update({
            "session": mock.Mock(spec=requests.Session),
            "serializer": slumber.serialize.Serializer(),
        })
        self.base_resource._store["session"].request.return_value = r

        resp = self.base_resource._request("PATCH")

        self.assertTrue(resp is r)
        self.assertEqual(resp.content, r.content)

        self.base_resource._store["session"].request.assert_called_once_with(
            "PATCH",
            "http://example/api/v1/test",
            data=None,
            params=None,
            headers={"content-type": self.base_resource._store["serializer"].get_content_type(), "accept": self.base_resource._store["serializer"].get_content_type()}
        )

        resp = self.base_resource.patch(data={'foo': 'bar'})
        self.assertEqual(resp['result'], ['a', 'b', 'c'])

    def test_put_201_redirect(self):
        r1 = mock.Mock(spec=requests.Response)
        r1.status_code = 201
        r1.headers = {"location": "http://example/api/v1/test/1"}
        r1.content = ''

        r2 = mock.Mock(spec=requests.Response)
        r2.status_code = 200
        r2.headers = {}
        r2.content = '{"result": ["a", "b", "c"]}'

        self.base_resource._store.update({
            "session": mock.Mock(spec=requests.Session),
            "serializer": slumber.serialize.Serializer(),
        })
        self.base_resource._store["session"].request.side_effect = (r1, r2)

        resp = self.base_resource._request("PUT")

        self.assertTrue(resp is r1)
        self.assertEqual(resp.content, r1.content)

        self.base_resource._store["session"].request.assert_called_once_with(
            "PUT",
            "http://example/api/v1/test",
            data=None,
            params=None,
            headers={"content-type": self.base_resource._store["serializer"].get_content_type(), "accept": self.base_resource._store["serializer"].get_content_type()}
        )

        resp = self.base_resource.put(data={'foo': 'bar'})
        self.assertEqual(resp['result'], ['a', 'b', 'c'])

    def test_put_decodable_response(self):
        r = mock.Mock(spec=requests.Response)
        r.status_code = 200
        r.content = '{"result": ["a", "b", "c"]}'
        r.headers = {}

        self.base_resource._store.update({
            "session": mock.Mock(spec=requests.Session),
            "serializer": slumber.serialize.Serializer(),
        })
        self.base_resource._store["session"].request.return_value = r

        resp = self.base_resource._request("PUT")

        self.assertTrue(resp is r)
        self.assertEqual(resp.content, r.content)

        self.base_resource._store["session"].request.assert_called_once_with(
            "PUT",
            "http://example/api/v1/test",
            data=None,
            params=None,
            headers={"content-type": self.base_resource._store["serializer"].get_content_type(), "accept": self.base_resource._store["serializer"].get_content_type()}
        )

        resp = self.base_resource.put(data={'foo': 'bar'})
        self.assertEqual(resp['result'], ['a', 'b', 'c'])
