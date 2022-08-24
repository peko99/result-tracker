# Copyright 2022 Marin Pejcin


from typing import Optional
from pydantic import BaseModel


class PlayerBase(BaseModel):
    username: Optional[str]
    email: Optional[str]
    team_id: Optional[int]


class PlayerCreate(PlayerBase):
    username: str
    email: str
    team_id: int


class PlayerUpdate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int

    class Config:
        orm_mode = True
