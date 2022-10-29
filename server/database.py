import sqlite3
from server.decoder import generate_key_pair
from server.utils import format_coordinates

con = sqlite3.connect("server/game_data.db")

cur = con.cursor()

def generate_tables():
    query = """
        CREATE TABLE GAME_DATA
        (GAME_ID INT,
        PLAYER_ID INT,
        COORDINATEs INT,
        UNIT_ID INT);
    """
    cur.execute(query)
    query = """
        CREATE TABLE GAME_KEY
        (GAME_ID INT,
        PRIVATE_KEY CHAR(255));
    """
    cur.execute(query)

# def store_initial_game_state(
#     game_id,
#     private_key,
#     player_id_1,
#     player_id_2,
#     player_id_3,
#     unit_id_1, 
#     unit_id_2, 
#     unit_id_3, 
#     location_1, 
#     location_2, 
#     location_3
# ):

#     query = f"""
#         INSERT INTO game_data (GAME_ID, PLAYER_ID, COORDINATE_X, COORDINATE_Y, UNIT_ID) 
#         VALUES 
#         ({game_id}, {private_key}, {player_id_1}, {location_1.x}, {location_1.y}, {unit_id_1}),
#         ({game_id}, {private_key}, {player_id_2}, {location_2.x}, {location_2.y}, {unit_id_2}),
#         ({game_id}, {private_key}, {player_id_3}, {location_3.x}, {location_3.y}, {unit_id_3}),
#     """
#     cur.execute(query)

def store_new_location(game_id, player_id, location):
    formatted_coordinates = format_coordinates(location.x, location.y)
    query = f"""
        UPDATE GAME_DATA
        SET COORDINATES = {formatted_coordinates}
        WHERE
            GAME_ID = {game_id}
            PLAYER_ID = {player_id}
    """
    cur.execute(query)
    

async def store_player_data(
    game_id,
    random_number,
    player_id,
    location,
    unit_id,
):
    formatted_coordinates = format_coordinates(location["x"], location["y"])
    query = f"""
        INSERT INTO GAME_DATA (GAME_ID, PLAYER_ID, COORDINATES, UNIT_ID) 
        VALUES 
        ({game_id}, {random_number}, {player_id}, {formatted_coordinates}, {unit_id}),
    """
    cur.execute(query)

def fetch_players(game_id):
    query = f"""
        SELECT PLAYER_ID FROM GAME_DATA WHERE GAME_ID={game_id}
    """
    cur.execute(query)
    players = cur.fetchmany()
    return players

def fetch_public_key(game_id):
    query = f"""
        SELECT PUBLIC_KEY FROM GAME_KEY WHERE GAME_ID={game_id}
    """
    cur.execute(query)
    public_key = cur.fetchone()
    return public_key

def fetch_private_key(game_id):
    query = f"""
        SELECT PRIVATE_KEY FROM GAME_KEY WHERE GAME_ID={game_id}
    """
    cur.execute(query)
    private_key = cur.fetchone()
    return private_key

def fetch_location(game_id, player_id):
    query = f"""
        SELECT COORDINATES FROM GAME_DATA WHERE GAME_ID={game_id} AND PLAYER_ID={player_id}
    """
    cur.execute(query)
    coordinates = cur.fetchone()
    return coordinates


async def start_game(game_id, random_1, random_2, random_3):
    seed = random_1 * random_2 * random_3
    private_key, public_key = generate_key_pair(seed)
    query = f"""
        INSERT INTO GAME_KEY (GAME_ID, PRIVATE_KEY, PUBLIC_KEY) 
        VALUES 
        ({game_id}, {private_key}, {public_key}),
    """
    cur.execute(query)


if __name__ == "__main__":
    generate_tables()
