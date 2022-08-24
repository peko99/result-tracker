# Copyright 2022 Marin Pejcin


from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.crud import crud_team
from dependencies import get_db
from core.schemas import Team, TeamCreate, TeamUpdate


router = APIRouter(prefix="/team", tags=["team"], dependencies=[Depends(get_db)])


@router.post("", response_model=Team)
async def create_team(team_in: TeamCreate, db: Session = Depends(get_db)) -> Any:
    try:
        created_team = crud_team.create(obj_in=team_in, db=db)
    except IntegrityError as _:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"Conflict on creating the team. Team with name {team_in.team_name} already exists.",
        )
    else:
        return created_team


@router.get("", response_model=List[Team])
async def get_teams(db: Session = Depends(get_db)) -> Any:
    return crud_team.get_all(db=db)


@router.get("/id/{id_}", response_model=Team)
async def get_team_by_id(id_: int, db: Session = Depends(get_db)) -> Any:
    team = crud_team.get(id_=id_, db=db)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found!")
    return team


@router.get("/team-name/{team_name}", response_model=Team)
async def get_team_by_team_name(team_name: str, db: Session = Depends(get_db)) -> Any:
    team = crud_team.get_by_team_name(team_name=team_name, db=db)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found!")
    return team


@router.put("{id_}", response_model=Team)
async def update_team(
    id_: int, team_in: TeamUpdate, db: Session = Depends(get_db)
) -> Any:
    team = crud_team.get(id_=id_, db=db)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found!")
    updated_team = crud_team.update(db_obj=team, obj_in=team_in, db=db)
    if not updated_team:
        raise HTTPException(status_code=409, detail="Team could not be updated")
    return updated_team


@router.delete("/{id_}", response_model=Team)
async def delete_team(id_: int, db: Session = Depends(get_db)) -> Any:
    team = crud_team.get(id_=id_, db=db)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found!")
    return crud_team.delete(id_=id_, db=db)
