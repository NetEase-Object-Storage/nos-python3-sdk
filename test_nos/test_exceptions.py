# -*- coding:utf8 -*-

from nos.exceptions import (ClientException, ServiceException,
                            InvalidObjectName, InvalidBucketName,
                            FileOpenModeError, MultiObjectDeleteException)

from .test_cases import TestCase


class TestClientException(TestCase):
    def test_default(self):
        message = "ClientException(hello) caused by: KeyError('key error')"
        err = KeyError("key error")
        exception = ClientException('hello', err)
        self.assertEqual('hello', exception.error)
        self.assertEqual(err, exception.info)
        self.assertEqual(message, exception.message)
        self.assertEqual(message, str(exception))


class TestServiceException(TestCase):
    def test_default(self):
        status_code = 400
        error_type = 'Bad Request'
        error_code = 'InvalidArgument'
        request_id = '9b8932d70aa000000154d729c6b0840e'
        message = 'uploadId=23r54i252358235-3253222'
        exception = ServiceException(status_code, error_type, error_code,
                                     request_id, message)
        self.assertEqual(status_code, exception.status_code)
        self.assertEqual(error_type, exception.error_type)
        self.assertEqual(error_code, exception.error_code)
        self.assertEqual(request_id, exception.request_id)
        self.assertEqual(message, exception.message)
        self.assertEqual(
            'ServiceException(400, Bad Request, InvalidArgument,'
            ' 9b8932d70aa000000154d729c6b0840e, '
            'uploadId=23r54i252358235-3253222)',
            str(exception))


class TestInvalidObjectName(TestCase):
    def test_default(self):
        message = 'InvalidObjectName caused by: object name is empty.'
        exception = InvalidObjectName()
        self.assertEqual(None, exception.error)
        self.assertEqual(None, exception.info)
        self.assertEqual(message, exception.message)
        self.assertEqual(message, str(exception))


class TestInvalidBucketName(TestCase):
    def test_default(self):
        message = 'InvalidBucketName caused by: bucket name is empty.'
        exception = InvalidBucketName()
        self.assertEqual(None, exception.error)
        self.assertEqual(None, exception.info)
        self.assertEqual(message, exception.message)
        self.assertEqual(message, str(exception))


class TestFileOpenModeError(TestCase):
    def test_default(self):
        message = ('FileOpenModeError caused by: object is a file that opened '
                   'without the mode for binary files.')
        exception = FileOpenModeError()
        self.assertEqual(None, exception.error)
        self.assertEqual(None, exception.info)
        self.assertEqual(message, exception.message)
        self.assertEqual(message, str(exception))


class TestMultiObjectDeleteException(TestCase):
    def test_default(self):
        info = [{
            'key': '2.jpg',
            'code': 'NoSuchKey',
            'message': 'No Such Key'
        }]
        message = ('MultiObjectDeleteException caused by: some objects delete '
                   'unsuccessfully.')
        exception = MultiObjectDeleteException(info)
        self.assertEqual(None, exception.status_code)
        self.assertEqual(None, exception.error_type)
        self.assertEqual(None, exception.error_code)
        self.assertEqual(None, exception.request_id)
        self.assertEqual(message, exception.message)
        self.assertEqual(info, exception.errors)
        self.assertEqual(
            "%s %s" % (message, info),
            str(exception)
        )
