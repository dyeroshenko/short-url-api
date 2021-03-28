from hashids import Hashids
from typing import Tuple

class Hashing:
    '''
    Hashes / decodes int or str values passed to respective methods using hashids library:
    https://hashids.org/
    '''
    def __init__(self):
        self.hash = Hashids(salt='xm0oswy23h')

    def generate_hash_key(self, id: int) -> str:
        '''
        Hashes parameter (int) and returns hashed value (str)
        '''
        hashed = self.hash.encode(id)
        return hashed

    def decode_hash_key(self, key: str) -> Tuple[int, None]:
        '''
        Takes str value encoded by [generate_hash_key()] and decodes it to int. Return format ([value:int], None)
        '''
        unhashed = self.hash.decode(key)
        return unhashed