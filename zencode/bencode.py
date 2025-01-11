from sys import byteorder
from collections.abc import Iterator

class Tokens:
    INT_START = b'i'
    LIST_START = b'l'
    DICT_START = b'd'
    STR_SEP = b':'
    END = b'e'


class Decoder:
    def __init__(self, data: bytes):
        self._data = data
        self._idx = 0

    def decode(self) -> int | str | list | dict:
        result = []

        # TODO: We need to find a way to determine corresponding
        # starting & ending characters. In other words, we need 
        # a way of knowing where a list ends. Which starting character
        # corresponding to an ending character. 

        '''
        decode(li1eei2e)
            | case Tokens.LIST_START
            | consume_next_byte()
            | decode_list([])
                | peek() != Tokens.END
                | decode()
                    | case Tokens.INT_START
                    | consume_next_byte()
                    | decode_int()
                        | read_until(Tokens.END)
                        | return b'1'        
        '''

        while self._idx < len(self._data):
            match self._peek():
                case Tokens.INT_START:
                    self._consume_next_byte()
                    result.append(self._decode_int())
                case Tokens.LIST_START:
                    self._consume_next_byte()
                    result.append(self._decode_list([]))
                    pass
                case Tokens.END:
                    self._consume_next_byte()
                case _:
                    result.append(self._decode_str())
                # case DICT_START_TOK:
                #     pass
        
        return result
    
    def _decode_list(self, result_list) -> list:
        if self._peek() != Tokens.END:
            result_list.extend(self.decode())
        return result_list
    
    def _decode_int(self) -> int:
        '''
        How to decode an int? 
            - Example: b'i1234e'
            1) We see an 'i' byte
            2) Consume this byte 
            3) Read until 'e' byte found, add each bit to a new byte
            4) Cast byte to int
        '''
        return int(self._read_until(Tokens.END))        
    
    def _decode_str(self):
        # Next byte must be a number...
        if not self._peek() in b'0123456789':
            raise ValueError(f'Invalid byte found at position {self._idx} while decoding str! Byte is {self._peek()}')
        
        try:
            str_len = int(self._read_until(Tokens.STR_SEP))
        except ValueError as err:
            print(f'Invalid string length found at position {self._idx}')

        # Consume string separator token...
        self._consume_next_byte()
        return self._consume_next_n_bytes(str_len).decode('utf-8')
                
    def _peek(self):
        return self._data[self._idx: self._idx + 1]
    
    def _consume_next_n_bytes(self, n: int) -> bytes:
        if self._idx >= len(self._data):
            raise IndexError("All bytes consumed!") 
        
        result = b''
        counter = 0

        while self._idx < len(self._data) and counter < n:
            result += self._consume_next_byte()
            counter += 1

        return result
    
    def _consume_next_byte(self) -> bytes:
        if self._idx >= len(self._data):
            raise IndexError("All bytes consumed!")
        
        result = self._data[self._idx: self._idx+1]
        self._idx += 1
        return result
    
    def _read_until(self, target_token: bytes) -> bytes:
        result = b''
        while self._idx < len(self._data) and self._peek() != target_token:
            result += self._consume_next_byte()
        return result
            
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
