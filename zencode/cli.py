
import argparse
from .bencode import Encoder

def main():
    parser = argparse.ArgumentParser(
        prog='zencode',
        description='bencode encoder/decoder',
    )
    parser.add_argument('filename')
    args = parser.parse_args()

    encoder = Encoder()
    test_objs = [
        12345,
        "test object",
        ["listObj1", 124123]
    ]
    for test_obj in test_objs:
        print(encoder.encode(test_obj))