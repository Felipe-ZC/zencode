
import argparse
from .bencode import Encoder, Decoder

ONE_BYTE = 1


def main():
    parser = argparse.ArgumentParser(
        prog='zencode',
        description='bencode encoder/decoder',
    )
    parser.add_argument('filename')
    args = parser.parse_args()

    # decoder = Decoder()
    print(Decoder(b'i1234e2:hi').decode())

    # print('Opening file with name: ', args.filename)

    # def read_next_byte ():
    #     with open(args.filename, 'rb') as f:
    #         while (byte := f.read(ONE_BYTE)):
    #             yield byte
    
    # for byte in read_next_byte():
    #     print(byte)

        # print(f.read())
        # # while (byte := f.read(ONE_BYTE)):
        # #     print(byte)


    # encoder = Encoder()
    # test_objs = [
    #     # 12345,
    #     # "test object",
    #     # ["listObj1", 124123],
    #     {
    #         # 'test_str': 'object',
    #         # 'test_int': 2,
    #         # 'test_list': ['object', 2],
    #         'test_dict': {
    #             'cow': 'moo',
    #             'spam': 'eggs'
    #         }
    #     }
    # ]
    # for test_obj in test_objs:
    #     print(encoder.encode(test_obj))
