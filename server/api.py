from fastapi import FastAPI
from server.decoder import hash_coordinates
from server.database import (
    start_game,
    store_player_data,
    fetch_players,
    fetch_public_key,
    store_new_location,
    fetch_location
)
from server.utils import decode_coordinates

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
    hashed_coord = hash_coordinates(combined_coordinates)
    return hashed_coord

@app.post("/set_player_data")
async def set_player(game_id, random_number, player_id, coordinate_x, coordinate_y, unit_id):
    coordinates = {
        "x": coordinate_x,
        "y": coordinate_y
    }
    store_player_data(game_id, random_number, player_id, coordinates, unit_id)
    # fetch players by game id, if 3 start game
    players = fetch_players(game_id)
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
