from pydantic import BaseModel

class Location(BaseModel):
    x: int
    y: int

class SetLocationBody(BaseModel):
    game_id: int
    player_id: int
    location: Location

class SetPlayerBody(BaseModel):
    game_id: int
    random_number: int
    player_id: int
    location: Location
    unit_id: int