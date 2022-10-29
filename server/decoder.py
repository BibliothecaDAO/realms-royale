import ecdsa
from ecdsa.util import PRNG
import hashlib

def hash_coordinates(seed, coordinates):
    encrypted_coordinates = seed * coordinates
    m = hashlib.sha256()
    b_coordinates = encrypted_coordinates.to_bytes(32, 'big')
    m.update(b_coordinates)
    print(m.hexdigest())
    return m.hexdigest()

def hash_unitid(seed, unit_id):
    encrypted_unit_id = seed * unit_id
    m = hashlib.sha256()
    b_coordinates = encrypted_unit_id.to_bytes(32, 'big')
    m.update(b_coordinates)
    print(m.hexdigest())
    return m.hexdigest()

# def verify_signature(game_id):
#     private_key = fetch_private_key(game_id)
#     vk = sk.get_verifying_key()
#     vk.verify(sig, id) # True

def generate_key_pair(seed):
    b_seed = seed.to_bytes(32, "big")
    random_number = PRNG(b_seed)
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, entropy=random_number)
    private_key = sk.to_string().hex()
    vk = sk.get_verifying_key()
    public_key = vk.to_string().hex()
    print(private_key)
    print(public_key)
    return private_key, public_key

if __name__ == "__main__":
    x = 2
    y = 1
    coordinates = x * 10000 + y
    hash_coordinates(123, coordinates)
    hash_unitid(123, 0)
    generate_key_pair(123)