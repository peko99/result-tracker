# Copyright 2022 Marin Pejcin


from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class GameBase(BaseModel):
    home_goals: Optional[int]
    away_goals: Optional[int]


class GameCreate(GameBase):
    home_team: int
    away_team: int
    date_played: datetime


class GameUpdate(GameBase):
    pass


class Game(GameBase):
    id: int
    home_team: int
    away_team: int
    date_played: datetime

    class Config:
        orm_mode = True
