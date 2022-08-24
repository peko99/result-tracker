# Copyright 2022 Marin Pejcin


from typing import Optional 
from pydantic import BaseModel


class TeamBase(BaseModel):
    team_name: Optional[str]
    goals_for: Optional[int]
    goals_against: Optional[int]


class TeamCreate(TeamBase):
    team_name: str
    goals_for: int
    goals_against: int


class TeamUpdate(TeamBase):
    pass


class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True
