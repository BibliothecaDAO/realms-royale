import sqlite3

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
    query = """
        SELECT GAME_ID, RANDOM_NUMBER, PLAYER_ID, COORDINATES, UNIT_ID FROM GAME_DATA
    """
    cur.execute(query)
    print(cur.fetchall())

if __name__ == "__main__":
    test_data()