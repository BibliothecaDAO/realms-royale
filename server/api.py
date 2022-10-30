import os
from fastapi import FastAPI
from server.decoder import hash_coordinates, calculate_movable_coordinates
from fastapi.middleware.cors import CORSMiddleware
from server.database import (
    fetch_seed,
    fetch_unit,
    start_game,
    store_player_data,
    fetch_players,
    fetch_public_key,
    store_new_location,
    fetch_location
)
from server.utils import decode_coordinates
from server.models import *

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_public_key")
async def read_item(game_id):
    public_key = fetch_public_key(game_id)
    return {"public_key": public_key}


@app.post("/set_location")
async def set_location(body: SetLocationBody):
    store_new_location(**body.dict())

@app.get("/get_location")
async def get_location(game_id, player_id):
    combined_coordinates = fetch_location(game_id, player_id)
    seed = fetch_seed(game_id)
    hashed_coord = hash_coordinates(seed, combined_coordinates)
    return hashed_coord

@app.get("/get_moveable_locations")
async def get_movable_locations(game_id, player_id):
    combined_coordinates = fetch_location(game_id, player_id)
    seed = fetch_seed(game_id)
    movable_coordinates = calculate_movable_coordinates(seed, combined_coordinates)
    return (movable_coordinates)

@app.get("/get_unit")
async def get_unit(game_id, player_id):
    unit_id = fetch_unit(game_id, player_id)
    seed = fetch_seed()
    hashed_unit_id = hash_coordinates(seed, unit_id)
    return hashed_unit_id

@app.post("/set_player_data")
async def set_player(body: SetPlayerBody):
    pre_players = fetch_players(body.game_id)
    player_id = len(pre_players) + 1
    await store_player_data(player_id, **body.dict())
    # fetch players by game id, if 3 start game
    post_players = fetch_players(body.game_id)
    if len(post_players) == 3:
        random_numbers = []
        for player in post_players:
            random_number = player[1]
            random_numbers.append(random_number)
        start_game(body.game_id, *random_numbers)
    # do the incrementing of players to the client
    return len(post_players)

@app.get("/reset_database")
async def reset_database():
    database_path = os.path.join(os.path.dirname(__file__), "..", "game_data.db")
    if os.path.isfile(database_path):
        os.remove(database_path)
        return "Database has been reset"
    else:
        return "Database is empty"


# @app.get("/verify_key")
# async def verify_key(public_key):
#     key_int = int(public_key)
#     sig = sk.sign


@app.get("/")
async def root():
    return {"message": "Hello World"}
