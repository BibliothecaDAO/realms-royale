from fastapi import FastAPI
from server.decoder import hash_coordinates
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


@app.get("/get_public_key")
async def read_item(game_id):
    public_key = fetch_public_key(game_id)
    return {"public_key": public_key}


@app.post("/set_location")
async def set_location(game_id, player_id, new_location):
    store_new_location(game_id, player_id, new_location)

@app.get("/get_location")
async def get_location(game_id, player_id):
    combined_coordinates = fetch_location(game_id, player_id)
    seed = fetch_seed()
    hashed_coord = hash_coordinates(seed, combined_coordinates)
    return hashed_coord

@app.get("/get_unit")
async def get_unit(game_id, player_id):
    unit_id = fetch_unit(game_id, player_id)
    seed = fetch_seed()
    hashed_unit_id = hash_coordinates(seed, unit_id)
    return hashed_unit_id

@app.post("/set_player_data")
async def set_player(body: SetPlayerBody):
    coordinates = {
        "x": body.coordinate_x,
        "y": body.coordinate_y
    }
    store_player_data(
        body.game_id,
        body.random_number,
        body.player_id,
        coordinates,
        body.unit_id,
    )
    # fetch players by game id, if 3 start game
    players = fetch_players(body.game_id)
    if len(players) == 3:
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
