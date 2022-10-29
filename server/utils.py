def format_coordinates(x, y):
    combined = x * 10000 + y
    return combined

def decode_coordinates(combined):
    x = combined / 10000
    y = combined % 10000
    return x, y

def convert_to_bytes(val):
    b_coordinates = bytes(val)
    return b_coordinates