import unittest

from zencode.bencode import Encoder

class EncoderTests(unittest.TestCase):

    encoder = Encoder()

    def test_empty_encoding(self):
        result, expected = self.encoder.encode(None), None
        self.assertEqual(result, expected)

    def test_int(self):
        result, expected = self.encoder.encode(12345), b'i12345e'
        self.assertEqual(result, expected)

    def test_str(self):
        result, expected = self.encoder.encode('zencode'), b'7:zencode'
        self.assertEqual(result, expected)

    def test_list(self):
        test_list = [
            12345,
            'onetwothreefour',
            {'test_key': 'test_val'}
        ]
        result, expected = self.encoder.encode(
            test_list), b'li12345e15:onetwothreefourd8:test_key8:test_valee'
        self.assertEqual(result, expected)

    def test_nested_list(self):
        test_list = [
            12345,
            'onetwothreefour',
            {'test_key': 'test_val'},
            [
                123456,
                'fivesix',
                {'test_key': 'test_val'},
            ]
        ]
        result, expected = self.encoder.encode(
            test_list), b'li12345e15:onetwothreefourd8:test_key8:test_valeli123456e7:fivesixd8:test_key8:test_valeee'
        self.assertEqual(result, expected)

    def test_dict_shallow(self):
        test_dict = {
            'a': 'b',
            'b': 4,
            'c': [1234]
        }
        result, expected = self.encoder.encode(
            test_dict), b'd1:a1:b1:bi4e1:cli1234eee'
        self.assertEqual(result, expected)

    def test_dict_nested(self):
        test_dict = {
            'a': 'b',
            'b': 4,
            'c': [1234],
            'd': { 'nested': 'structure' }
        }
        result, expected = self.encoder.encode(
            test_dict), b'd1:a1:b1:bi4e1:cli1234ee1:dd6:nested9:structureee'
        self.assertEqual(result, expected)