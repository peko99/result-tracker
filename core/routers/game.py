# Copyright 2022 Marin Pejcin


from time import sleep
from typing import Any, List
from core.schemas.team import TeamCreate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.crud import crud_game, crud_team
from dependencies import get_db
from core.schemas import Game, GameCreate, GameUpdate


router = APIRouter(prefix="/game", tags=["game"], dependencies=[Depends(get_db)])


@router.post("", response_model=Game)
async def create_game(game_in: GameCreate, db: Session = Depends(get_db)) -> Any:
    if game_in.home_team == game_in.away_team:
        raise HTTPException(
            status_code=400, detail="Home and away team can not be the same!"
        )
    if isinstance(game_in.home_team, str):
        home_team = crud_team.get_by_team_name(team_name=game_in.home_team, db=db)
        if not home_team:
            home_team = crud_team.create(obj_in=TeamCreate(team_name=game_in.home_team), db=db)
        game_in.home_team = home_team.id
    else:
        home_team = crud_team.get(id_=game_in.home_team, db=db)
    if isinstance(game_in.away_team, str):
        away_team = crud_team.get_by_team_name(team_name=game_in.away_team, db=db)
        if not away_team:
            away_team = crud_team.create(obj_in=TeamCreate(team_name=game_in.away_team), db=db)
        game_in.away_team = away_team.id
    else:
        away_team = crud_team.get(id_=game_in.away_team, db=db)
    crud_team.update_stats(
        home_team=home_team, away_team=away_team, game_in=game_in, db=db
    )
    try:
        created_game = crud_game.create(obj_in=game_in, db=db)
    except IntegrityError as _:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"Conflict on creating a game.",
        )
    else:
        return created_game


@router.get("", response_model=List[Game])
async def get_games(db: Session = Depends(get_db)) -> Any:
    return crud_game.get_all(db=db)


@router.get("/id/{id_}", response_model=Game)
async def get_game_by_id(id_: int, db: Session = Depends(get_db)) -> Any:
    game = crud_game.get(id_=id_, db=db)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found!")
    return game


@router.get("/team/{team_id}", response_model=List[Game])
async def get_games_by_team(team_id: int, db: Session = Depends(get_db)) -> Any:
    team = crud_team.get(id_=team_id, db=db)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found!")
    return crud_game.get_games_by_team(team_id=team_id, db=db)


@router.put("/{id_}", response_model=Game)
async def update_game(
    id_: int, game_in: GameUpdate, db: Session = Depends(get_db)
) -> Any:
    game = crud_game.get(id_=id_, db=db)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found!")
    try:
        updated_game = crud_game.update(db_obj=game, obj_in=game_in, db=db)
    except IntegrityError as _:
        raise HTTPException(status_code=409, detail="Game could not be updated!")
    return updated_game


@router.delete("/{id_}", response_model=Game)
async def delete_game(id_: int, db: Session = Depends(get_db)) -> Any:
    game = crud_game.get(id_=id_, db=db)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found!")
    return crud_game.delete(id_=id_, db=db)
