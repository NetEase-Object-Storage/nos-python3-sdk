# -*- coding:utf8 -*-

from mock import Mock
from nos.client.auth import RequestMetaData

from ..test_cases import TestCase


class TestRequestMetaData(TestCase):
    def test_get_url(self):
        meta_data = RequestMetaData('', '', 'GET')
        meta_data.url = 'http://www.1.com'
        self.assertEqual('http://www.1.com', meta_data.get_url())

    def test_get_headers(self):
        meta_data = RequestMetaData('', '', 'GET')
        meta_data.headers = {'a': 'b'}
        self.assertEqual({'a': 'b'}, meta_data.get_headers())

    def test_complete_headers(self):
        meta_data = RequestMetaData('', '', 'GET', body='1234567')
        self.assertEqual('fcea920f7412b5da7be0cf42b8c93759',
                          meta_data.headers['Content-MD5'])

        meta_data = RequestMetaData('', '', 'GET', body='1234567')
        meta_data._get_string_to_sign = Mock(return_value='12345')
        meta_data._complete_headers()
        self.assertEqual('NOS :riPI9XPTbHodbLyLC+vlLgZm3PFPoEQHMo+5RLj3qC0=',
                          meta_data.headers['Authorization'])

        meta_data = RequestMetaData('test', 'object', 'GET', 'aaa', 'bbb',
                                    params={'upload': None, 'a': 12345})
        self.assertEqual('http://aaa.nos.netease.com/bbb?a=12345&upload',
                          meta_data.url)

    def test_get_string_to_sign(self):
        meta_data = RequestMetaData('', '', 'GET')
        meta_data.headers = {
            'Date': 'Fri, 10 Feb 2012 21:34:55 GMT',
            'Expires': 'Fri, 10 Feb 2016 21:34:55 GMT',
            'x-nos-x': 'hello'
        }
        meta_data._get_canonicalized_resource = Mock(return_value='12345')
        self.assertEqual(
            'GET\n\n\nFri, 10 Feb 2016 21:34:55 GMT\nx-nos-x:hello\n12345',
            meta_data._get_string_to_sign()
        )

    def test_get_canonicalized_resource(self):
        meta_data = RequestMetaData('', '', 'GET')
        meta_data.bucket = 'test'
        meta_data.key = 'ob&2!'
        meta_data.params = {
            'test': '1',
            'a': 2,
            'upload': None,
            'logging': 3,
            'lifecycle': None,
            'delete': None,
            'uploadId': '1221334'
        }
        self.assertEqual(
            '/test/ob%262%21?delete&uploadId=1221334',
            meta_data._get_canonicalized_resource()
        )
