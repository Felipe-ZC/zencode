class Encoder:
    """
    A class representing a bencode encoder. Can be used to encode python objects into bencode.
    Supported types are:
        - str
        - int
        - list
        - dict
    """

    def encode(self, data) -> bytes:
        match data:
            case int():
                return self.encode_int(data)
            case str():
                return self.encode_str(data)
            case list():
                return self.encode_list(data)
            case dict():
                return self.encode_dict(data)
            case _:
                return None

    def encode_int(self, data) -> bytes:
        return bytes(f'i{data}e', encoding='ascii')

    def encode_str(self, data) -> bytes:
        return bytes(f'{len(data)}:{data}', encoding='ascii')

    def encode_dict(self, data) -> bytes:
        result = b'd'

        try:
            for key, value in data.items():
                encoded_key = self.encode(key)
                encoded_val = self.encode(value)

                if not isinstance(key, str):
                    raise ValueError(f'dict key is not a string! Key is {key}')

                if not encoded_key or not encoded_val:
                    raise ValueError(f'Invalid key, value pair: {key},{value}')

                result += encoded_key + encoded_val
        except (TypeError, ValueError) as err:
            raise err

        return result + b'e'

    def encode_list(self, data) -> bytes:
        return b'l' + b''.join([self.encode(obj) for obj in data]) + b'e'
