
class Encoder:
    """
    A class representing a bencode encoder. Can be used to encode python objects into bencode.
    Supported types are:
        - str
        - int
        - list
        - dict
        - bytes

    Attributes:
        
    """
    def encode(self, data) -> bytes:
        match data:
            case int():
                return self.encode_int(data)
            case str():
                return self.encode_str(data)
            case list():
                # return self.encode_list_iter(data)
                return self.encode_list_rec(b'', data, 0)
            case dict():
                return self.encode_dict(data)
            case _:
                print('invalid type')
        
    def encode_int(self, data) -> bytes:
        return bytes(f'i{data}e', encoding='ascii')
    
    def encode_str(self, data) -> bytes:
        return bytes(f'{len(data)}:{data}', encoding='ascii')
    
    def encode_dict(self, data) -> bytes:
        
    
    def encode_list_iter(self, data) -> bytes:
        return b'l' + b''.join([self.encode(obj) for obj in data]) + b'e'
    
    def encode_list_rec(self, bytes_list, data, idx) -> bytes:
        if idx >=  len(data):
            return b'l' + bytes_list + b'e'
        else:
            bytes_list += self.encode(data[idx])
            return self.encode_list_rec(bytes_list, data, idx + 1)
        