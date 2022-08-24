# Copyright 2022 Marin Pejcin


from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.crud import crud_player, crud_team
from dependencies import get_db
from core.schemas import Player, PlayerCreate, PlayerUpdate


router = APIRouter(prefix="/player", tags=["player"], dependencies=[Depends(get_db)])


@router.post("", response_model=Player)
async def create_player(player_in: PlayerCreate, db: Session = Depends(get_db)) -> Any:
    team = crud_team.get(id_=player_in.team_id, db=db)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    try:
        created_player = crud_player.create(obj_in=player_in, db=db)
    except IntegrityError as _:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"Conflict on creating a player, player with {player_in.username} already exists",
        )
    else:
        return created_player


@router.get("", response_model=List[Player])
async def get_players(db: Session = Depends(get_db)) -> Any:
    return crud_player.get_all(db=db)


@router.get("/id/{id_}", response_model=Player)
async def get_player_by_id(id_: int, db: Session = Depends(get_db)) -> Any:
    player = crud_player.get(id_=id_, db=db)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.get("/username/{username}", response_model=Player)
async def get_player_by_username(username: str, db: Session = Depends(get_db)) -> Any:
    player = crud_player.get_by_username(username=username, db=db)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.put("/{id_}", response_model=Player)
async def update_player(
    id_: int, player_in: PlayerUpdate, db: Session = Depends(get_db)
) -> Any:
    player = crud_player.get(id_=id_, db=db)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found!")
    if player_in.team_id:
        team = crud_team.get(id_=player_in.team_id, db=db)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
    updated_player = crud_player.update(db_obj=player, obj_in=player_in, db=db)
    if not updated_player:
        raise HTTPException(status_code=409, detail="Player could not be updated!")
    return updated_player


@router.delete("/{id_}", response_model=Player)
async def delete_player(id_: int, db: Session = Depends(get_db)) -> Any:
    player = crud_player.get(id_=id_, db=db)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found!")
    return crud_player.delete(id_=id_, db=db)
