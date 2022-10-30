import ecdsa
from ecdsa.util import PRNG
import hashlib
from server.utils import decode_coordinates, encode_coordinates

def hash_coordinates(seed, coordinates):
    print(coordinates)
    encrypted_coordinates = seed * coordinates
    print(f"encrypted coordinates: {encrypted_coordinates}")
    m = hashlib.sha256()
    b_coordinates = encrypted_coordinates.to_bytes(32, 'big')
    m.update(b_coordinates)
    return m.hexdigest()

def hash_unitid(seed, unit_id):
    encrypted_unit_id = seed * unit_id
    m = hashlib.sha256()
    b_coordinates = encrypted_unit_id.to_bytes(32, 'big')
    m.update(b_coordinates)
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
    return private_key, public_key

def adjacency_offsets():
    movables = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if (x == 0 and y == 0):
                break
            movables.append({ "x": x, "y": y})
    return movables

def calculate_movable_coordinates(seed, combined_coordinates):
    x0, y0 = decode_coordinates(combined_coordinates)
    offsets = adjacency_offsets()
    movable_coords = []
    for offset in offsets:
        nearby_x = offset["x"] + x0
        nearby_y = offset["y"] + y0
        if (nearby_x < 0 or nearby_y < 0 or nearby_x > 19 or nearby_y > 19):
            continue
        encoded_nearby = encode_coordinates(nearby_x, nearby_y)
        hash_nearby = hash_coordinates(seed, encoded_nearby)
        movable_coords.append({"x": nearby_x, "y": nearby_y, "hash": hash_nearby})
    return movable_coords


if __name__ == "__main__":
    # x = 2
    # y = 1
    # coordinates = x * 10000 + y
    # hash_coordinates(123, coordinates)
    # hash_unitid(123, 0)
    # generate_key_pair(123)
    # coord_offsets = adjacency_offsets()
    # hash_coordinates(
    calculate_movable_coordinates(5, 10000)