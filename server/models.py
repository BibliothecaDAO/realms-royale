from pydantic import BaseModel

class SetPlayerBody(BaseModel):
    game_id: int
    random_number: int
    player_id: int
    coordinate_x: int
    coordinate_y: int
    unit_id: int