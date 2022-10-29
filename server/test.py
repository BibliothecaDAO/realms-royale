import sqlite3
from server.decoder import hash_coordinates
from server.database import fetch_location

con = sqlite3.connect("game_data.db")

cur = con.cursor()

def test_data():
    query = """
        SELECT GAME_ID, RANDOM_NUMBER, PLAYER_ID, COORDINATES, UNIT_ID FROM GAME_DATA
    """
    cur.execute(query)
    print(cur.fetchall())

def test_data_2():
    query = f"""
        INSERT INTO GAME_DATA (GAME_ID, RANDOM_NUMBER, PLAYER_ID, COORDINATES, UNIT_ID) 
        VALUES 
        (1, 4, 1, 8, 0);
    """
    cur.execute(query)
    con.commit()
    query = """
        SELECT GAME_ID, RANDOM_NUMBER, PLAYER_ID, COORDINATES, UNIT_ID FROM GAME_DATA
    """
    cur.execute(query)
    print(cur.fetchall())

def test_location():
    location = fetch_location(1, 1)
    print(location)



if __name__ == "__main__":
    test_data_2()