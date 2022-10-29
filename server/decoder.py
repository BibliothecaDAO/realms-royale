import ecdsa
# from database import get_private_key
import hashlib
from server.utils import convert_to_bytes

def hash_coordinates(private_key, coordinates):
    m = hashlib.sha256()
    b_coordinates = convert_to_bytes(coordinates)
    m.update(b_coordinates)
    m.hexdigest()

def hash_unitid(id):
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) 
    vk = sk.get_verifying_key()
    sig = sk.sign(id)
    vk.verify(sig, id) # True

def verify_signature(sig):
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) 
    vk = sk.get_verifying_key()
    vk.verify(sig, id) # True

def generate_key_pair(seed):
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, entropy=seed)
    private_key = sk.to_string().hex()
    vk = sk.get_verifying_key()
    public_key = vk.to_string().hex()
    return private_key, public_key

if __name__ == "__main__":
    hash_coordinates(123)