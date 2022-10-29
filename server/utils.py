def encode_coordinates(x, y):
    combined = x * 10000 + y
    return combined

def decode_coordinates(combined):
    x = int(combined / 10000)
    y = combined % 10000
    return x, y

# def convert_to_bytes(val):
#     b_coordinates = bytes(val)
#     return b_coordinates

if __name__ == "__main__":
    encoded_coordinates = encode_coordinates(1, 1)
    decoded_coordinates = decode_coordinates(encoded_coordinates)
    print(decoded_coordinates)