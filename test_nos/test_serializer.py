# -*- coding:utf8 -*-

import uuid
from nos.serializer import JSONSerializer
from nos.exceptions import SerializationError
from datetime import date, datetime
from decimal import Decimal
from mock import Mock
from io import IOBase

from .test_cases import TestCase


class TestJSONSerializer(TestCase):
    def test_default(self):
        serializer = JSONSerializer()
        self.assertEqual('2016-05-01', serializer.default(date(2016, 5, 1)))
        self.assertEqual('2016-05-01T00:00:00',
                          serializer.default(datetime(2016, 5, 1)))
        self.assertEqual(12345.0, serializer.default(Decimal(12345)))
        self.assertEqual(
            '12345678-1234-5678-1234-567812345678',
            serializer.default(uuid.UUID('12345678123456781234567812345678'))
        )
        self.assertRaises(TypeError, serializer.default, 'sads')

    def test_dumps(self):
        serializer = JSONSerializer()
        self.assertEqual('12345', serializer.dumps('12345'))
        self.assertEqual('54321', serializer.dumps('54321'))
        s = Mock(spec=IOBase)
        self.assertEqual(s, serializer.dumps(s))
        self.assertEqual('{"a": "b"}', serializer.dumps({'a': 'b'}))
        self.assertRaises(SerializationError, serializer.dumps, set(['sadsa']))
