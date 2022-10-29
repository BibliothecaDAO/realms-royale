from fastapi import FastAPI
import sqlite3
from decoder import generate_key_pair
from database import (
    insert_data,
    start_game,
    store_player_data,
    get_players,
    get_public_key,
    store_new_location,
    get_location
)
from utils import decode_coordinates

app = FastAPI()


@app.get("/block_time")
async def read_item():
    return {"block_time": 100}


@app.get("/get_public_key")
async def read_item(game_id):
    public_key = get_public_key(game_id)
    return {"public_key": public_key}


@app.post("/set_location")
async def set_location(game_id, player_id, new_location):
    store_new_location(game_id, player_id, new_location)

@app.get("/get_location")
async def get_location(game_id, player_id):
    combined_coordinates = get_location(game_id, player_id)
    hash_coordinates()
    return 

@app.post("/join_lobby")
async def join_lobby(game_id, random_number, player_id, location, unit_id):
    store_player_data(game_id, random_number, player_id, location, unit_id)
    # fetch players by game id, if 3 start game
    players = get_players(game_id)
    if len(players) >= 3:
        start_game()

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_()
#         await websocket.send_text(f"Message text was: {data}")


@app.get("/")
async def root():
    return {"message": "Hello World"}


# async def check_coordinates(message_coordinates):
#     get_coordinates = read_starknet()

#     if (coordinates - location_coordinates < 1):
#         return (true)
#     else:
#         return (false)
