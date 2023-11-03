import unittest
import datetime
from decimal import Decimal
import uuid
from collections.abc import Mapping, Iterable
from enum import Enum
import giga_json as json

""" test all the things! """


class MyEnum(Enum):
    A = 1
    B = 2

class CustomObject:
    def _asdict(self):
        return {'giga_key': 'giga_value'}

# Test class
class CustomJSONEncoderTestCase(unittest.TestCase):
    def test_date(self):
        date = datetime.date(2023, 4, 1)
        self.assertEqual(json.dumps(date), '"2023-04-01"')

    def test_datetime(self):
        dt = datetime.datetime(2023, 4, 1, 12, 0)
        self.assertEqual(json.dumps(dt), '"2023-04-01T12:00:00"')

    def test_decimal(self):
        dec = Decimal('12.34')
        self.assertEqual(json.dumps(dec), '12.34')

    def test_uuid(self):
        u = uuid.uuid4()
        self.assertEqual(json.dumps(u), '"' + str(u) + '"')

    def test_mapping(self):
        m = {'a': 1, 'b': 2}
        self.assertEqual(json.dumps(m), '{\n    "a": 1,\n    "b": 2\n}')

    def test_iterable(self):
        l = [1, 2, 3]
        self.assertEqual(json.dumps(l), '[\n    1,\n    2,\n    3\n]')

    def test_bytes(self):
        b = b'hello'
        self.assertEqual(json.dumps(b), '"hello"')

    def test_set(self):
        s = {1, 2, 3}
        self.assertEqual(json.dumps(s), '[\n    1,\n    2,\n    3\n]')

    def test_complex(self):
        c = 1 + 2j
        self.assertEqual(json.dumps(c), '{\n    "imag": 2.0,\n    "real": 1.0\n}')

    def test_asdict(self):
        obj = CustomObject()
        self.assertEqual(json.dumps(obj), '{\n    "giga_key": "giga_value"\n}')

    def test_enum(self):
        self.assertEqual(json.dumps(MyEnum.A), '1')

    def test_fallback_to_str(self):
        obj = object()
        self.assertTrue(isinstance(json.dumps(obj), str))


if __name__ == '__main__':
    unittest.main()
