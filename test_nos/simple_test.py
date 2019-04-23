# -*- coding:utf8 -*-


import unittest
import hashlib
import json
import nos
import test_nos.test_config as Config


class SimpleTest(unittest.TestCase):
    ACCESS_KEY_ID = Config.ACCESS_KEY_ID
    ACCESS_KEY_SECRET =Config.ACCESS_KEY_SECRET
    BUCKET = Config.BUCKET
    KEYS = [
        '1特殊 字符`-=[]\\;\',./ ~!@#$%^&*()_+{}|:<>?"',
        '2特殊 字符`-=[]\\;\',./ ~!@#$%^&*()_+{}|:<>?"',
        '3特殊 字符`-=[]\\;\',./ ~!@#$%^&*()_+{}|:<>?"',
        '4特殊 字符`-=[]\\;\',./ ~!@#$%^&*()_+{}|:<>?"',
    ]
    BODY_STR = 'This is a test string!\r\n\r\n'
    BODY_DICT = {"a": 1, "b": 2, "c": 3}
    BODY_LIST = ["a", "b", "c"]


    def test_nos_client_https(self):
        info = {}

        # create client
        client = nos.Client(
            access_key_id=self.ACCESS_KEY_ID,
            access_key_secret=self.ACCESS_KEY_SECRET,
            enable_ssl=True
        )

        # put invalid object name
        self.assertRaises(nos.exceptions.InvalidObjectName,
                          client.put_object, Config.BUCKET, '', '')

        # put invalid bucket name
        self.assertRaises(nos.exceptions.InvalidBucketName,
                          client.put_object, '', 'bb', '')

        # put object
        r = client.put_object(self.BUCKET, self.KEYS[0], self.BODY_STR,
                              meta_data={'x-nos-meta-hello': 'world'})
        p_md5 = r['etag']

        # get object
        r = client.get_object(self.BUCKET, self.KEYS[0])
        g_md5 = r['etag']
        body = r['body'].read()

        # head object
        r = client.head_object(self.BUCKET, self.KEYS[0])
        h_md5 = r['etag']

        b_str = self.BODY_STR
        md5_str = hashlib.md5(b_str.encode('utf8')).hexdigest()
        info[self.KEYS[0]] = md5_str
        self.assertEqual(h_md5, md5_str)
        self.assertEqual(g_md5, md5_str)
        self.assertEqual(p_md5, md5_str)
        self.assertEqual(b_str, str(body,'utf8'))

        # put object
        r = client.put_object(self.BUCKET, self.KEYS[1], self.BODY_DICT)
        p_md5 = r['etag']

        # get object
        r = client.get_object(self.BUCKET, self.KEYS[1])
        g_md5 = r['etag']
        body = r['body'].read()

        # head object
        r = client.head_object(self.BUCKET, self.KEYS[1])
        h_md5 = r['etag']

        b_dict = json.dumps(self.BODY_DICT)
        md5_dict = hashlib.md5(b_dict.encode('utf8')).hexdigest()
        info[self.KEYS[1]] = md5_dict
        self.assertEqual(h_md5, md5_dict)
        self.assertEqual(g_md5, md5_dict)
        self.assertEqual(p_md5, md5_dict)
        self.assertEqual(b_dict, str(body,'utf8'))

        # put object
        r = client.put_object(self.BUCKET, self.KEYS[2], self.BODY_LIST)
        p_md5 = r['etag']

        # get object
        r = client.get_object(self.BUCKET, self.KEYS[2])
        g_md5 = r['etag']
        body = r['body'].read()

        # head object
        r = client.head_object(self.BUCKET, self.KEYS[2])
        h_md5 = r['etag']

        b_list = json.dumps(self.BODY_LIST)
        md5_list = hashlib.md5(b_list.encode('utf8')).hexdigest()
        info[self.KEYS[2]] = md5_list
        self.assertEqual(h_md5, md5_list)
        self.assertEqual(g_md5, md5_list)
        self.assertEqual(p_md5, md5_list)
        self.assertEqual(b_list, str(body,'utf8'))

        # list objects
        r = client.list_objects(
            bucket=self.BUCKET
        )
        resp = r['response']
        for i in resp.findall('Contents'):
            self.assertEqual(
                info[i.findtext('Key')],
                i.findtext('ETag').strip('"')
            )

        # move object
        r = client.move_object(
            self.BUCKET,
            self.KEYS[0],
            self.BUCKET,
            self.KEYS[3]
        )
        info[self.KEYS[3]] = info.pop(self.KEYS[0])

        # list objects
        r = client.list_objects(
            bucket=self.BUCKET
        )
        resp = r['response']
        for i in resp.findall('Contents'):
            self.assertEqual(
                info[i.findtext('Key')],
                i.findtext('ETag').strip('"')
            )

        # copy object
        r = client.copy_object(
            self.BUCKET,
            self.KEYS[1],
            self.BUCKET,
            self.KEYS[0]
        )
        info[self.KEYS[0]] = info[self.KEYS[1]]

        # list objects
        r = client.list_objects(
            bucket=self.BUCKET
        )
        resp = r['response']
        for i in resp.findall('Contents'):
            self.assertEqual(
                info[i.findtext('Key')],
                i.findtext('ETag').strip('"')
            )

        # delete object
        r = client.delete_object(
            self.BUCKET,
            self.KEYS[3]
        )
        info.pop(self.KEYS[3], '')
        self.assertRaises(nos.exceptions.NotFoundError, client.head_object,
                          self.BUCKET, self.KEYS[3])

        # list objects
        r = client.list_objects(
            bucket=self.BUCKET
        )
        resp = r['response']
        for i in resp.findall('Contents'):
            self.assertEqual(
                info[i.findtext('Key')],
                i.findtext('ETag').strip('"')
            )

        # delete objects
        r = client.delete_objects(
            self.BUCKET,
            [self.KEYS[1], self.KEYS[2]]
        )
        self.assertRaises(nos.exceptions.BadRequestError,
                          client.delete_objects, self.BUCKET, [])
        self.assertRaises(nos.exceptions.MultiObjectDeleteException,
                          client.delete_objects, self.BUCKET, [self.KEYS[3]])
        info.pop(self.KEYS[1], '')
        info.pop(self.KEYS[2], '')
        info.pop(self.KEYS[3], '')
        self.assertRaises(nos.exceptions.NotFoundError, client.head_object,
                          self.BUCKET, self.KEYS[1])
        self.assertRaises(nos.exceptions.NotFoundError, client.head_object,
                          self.BUCKET, self.KEYS[2])
        self.assertRaises(nos.exceptions.NotFoundError, client.head_object,
                          self.BUCKET, self.KEYS[3])

        # list objects
        r = client.list_objects(
            bucket=self.BUCKET
        )
        resp = r['response']
        for i in resp.findall('Contents'):
            self.assertEqual(
                info[i.findtext('Key')],
                i.findtext('ETag').strip('"')
            )

        # head object
        client.head_object(
            bucket=self.BUCKET,
            key=self.KEYS[0]
        )


if __name__ == "__main__":
    unittest.main()
