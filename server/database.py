import sqlite3
from server.decoder import generate_key_pair
from server.utils import decode_coordinates, encode_coordinates
from server.models import *

con = sqlite3.connect("game_data.db")

cur = con.cursor()

def generate_tables():
    query = """
        CREATE TABLE GAME_DATA
        (GAME_ID INT,
        RANDOM_NUMBER INT,
        PLAYER_ID INT,
        COORDINATES INT,
        UNIT_ID INT);
    """
    cur.execute(query)
    query = """
        CREATE TABLE GAME_KEY
        (GAME_ID INT,
        SEED INT,
        PRIVATE_KEY TEXT,
        PUBLIC_KEY TEXT);
    """
    cur.execute(query)

def store_new_location(
    game_id: int,
    player_id: int,
    location: Location,
):
    encoded_coordinates = encode_coordinates(location["x"], location["y"])
    query = f"""
        UPDATE GAME_DATA
        SET COORDINATES = {encoded_coordinates}
        WHERE
            GAME_ID = {game_id}
            AND
            PLAYER_ID = {player_id}
    """
    cur.execute(query)
    con.commit()
    

async def store_player_data(
    player_id: int,
    game_id: int,
    random_number: int,
    location: Location,
    unit_id: int,
):
    formatted_coordinates = encode_coordinates(location["x"], location["y"])
    query = f"""
        INSERT INTO GAME_DATA (GAME_ID, RANDOM_NUMBER, PLAYER_ID, COORDINATES, UNIT_ID) 
        VALUES 
        ({game_id}, {random_number}, {player_id}, {formatted_coordinates}, {unit_id});
    """
    cur.execute(query)
    con.commit()

def start_game(
        game_id: int, 
        random_1: int, 
        random_2: int, 
        random_3: int
    ):
    seed = random_1 * random_2 * random_3
    private_key, public_key = generate_key_pair(seed)
    query = f"""
        INSERT INTO GAME_KEY (GAME_ID, SEED, PRIVATE_KEY, PUBLIC_KEY) 
        VALUES (?,?,?,?);
    """
    cur.execute(query, (game_id, seed, private_key, public_key))
    con.commit()

def fetch_players(game_id: int):
    query = f"""
        SELECT PLAYER_ID, RANDOM_NUMBER FROM GAME_DATA WHERE GAME_ID={game_id}
    """
    cur.execute(query)
    players = cur.fetchall()
    return players

def fetch_seed(game_id: int):
    query = f"""
        SELECT SEED FROM GAME_KEY WHERE GAME_ID={game_id}
    """
    cur.execute(query)
    seed = cur.fetchone()
    return seed[0]

def fetch_public_key(game_id: int):
    query = f"""
        SELECT PUBLIC_KEY FROM GAME_KEY WHERE GAME_ID={game_id}
    """
    cur.execute(query)
    public_key = cur.fetchone()
    return public_key

def fetch_private_key(game_id: int):
    query = f"""
        SELECT PRIVATE_KEY FROM GAME_KEY WHERE GAME_ID={game_id}
    """
    cur.execute(query)
    private_key = cur.fetchone()
    return private_key

def fetch_location(
        game_id: int, 
        player_id: int
    ):
    query = f"""
        SELECT COORDINATES FROM GAME_DATA WHERE GAME_ID={game_id} AND PLAYER_ID={player_id}
    """
    cur.execute(query)
    coordinates = cur.fetchone()
    return coordinates[0]

def fetch_unit(
        game_id: int, 
        player_id: int
    ):
    query = f"""
        SELECT UNIT_ID FROM GAME_DATA WHERE GAME_ID={game_id} AND PLAYER_ID={player_id}
    """
    cur.execute(query)
    coordinates = cur.fetchone()
    return coordinates

def fetch_player_at_location(game_id: int, coordinates: int):
    query = f"""
        SELECT COORDINATES FROM GAME_DATA WHERE GAME_ID={game_id} AND COORDINATES={coordinates}
    """
    cur.execute(query)
    player_coordinates = cur.fetchone()
    if player_coordinates:
        x, y = decode_coordinates(player_coordinates[0])
        return (x, y)
    else:
        return None


if __name__ == "__main__":
    generate_tables()
