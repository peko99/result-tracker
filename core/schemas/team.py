# Copyright 2022 Marin Pejcin


from typing import Optional, List
from pydantic import BaseModel, validator

from core.schemas import Player


class TeamBase(BaseModel):
    team_name: Optional[str]
    wins: Optional[int] = 0
    draws: Optional[int] = 0
    losses: Optional[int] = 0
    goals_for: Optional[int] = 0
    goals_against: Optional[int] = 0
    games_played: Optional[int]
    points: Optional[int] = 0

    @validator("points", always=True, check_fields=False)
    def calculate_points(cls, v, values, **kwargs):
        return 3 * values["wins"] + values["draws"]

    @validator("games_played", always=True, check_fields=False)
    def calculate_games_played(cls, v, values, **kwargs):
        return values["wins"] + values["draws"] + values["losses"]


class TeamCreate(TeamBase):
    team_name: str


class TeamUpdate(TeamBase):
    pass


class Team(TeamBase):
    id: int
    players: List[Player]

    class Config:
        orm_mode = True
