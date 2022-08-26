# Copyright 2022 Marin Pejcin


from time import sleep
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.crud import crud_game, crud_team
from dependencies import get_db
from core.schemas import Game, GameCreate, GameUpdate, TeamUpdate


router = APIRouter(prefix="/game", tags=["game"], dependencies=[Depends(get_db)])


@router.post("", response_model=Game)
async def create_game(game_in: GameCreate, db: Session = Depends(get_db)) -> Any:
    if game_in.home_team == game_in.away_team:
        raise HTTPException(
            status_code=400, detail="Home and away team can not be the same team!"
        )
    home_team = crud_team.get(id_=game_in.home_team, db=db)
    if not home_team:
        raise HTTPException(status_code=404, detail="Home team not found!")
    home_team_update = TeamUpdate()
    away_team = crud_team.get(id_=game_in.away_team, db=db)
    if not away_team:
        raise HTTPException(status_code=404, detail="Away team not found!")
    away_team_update = TeamUpdate()
    if game_in.home_goals > game_in.away_goals:
        home_team_update.wins = home_team.wins + 1
        away_team_update.losses = away_team.losses + 1
    if game_in.home_goals < game_in.away_goals:
        home_team_update.losses = home_team.losses + 1
        away_team_update.wins = away_team.wins + 1
    if game_in.home_goals == game_in.away_goals:
        home_team_update.draws = home_team.draws + 1
        away_team_update.draws = away_team.draws + 1
    home_team_update.goals_for = home_team.goals_for + game_in.home_goals
    home_team_update.goals_against = home_team.goals_against + game_in.away_goals
    away_team_update.goals_for = away_team.goals_for + game_in.away_goals
    away_team_update.goals_against = away_team.goals_against + game_in.home_goals
    crud_team.update(db_obj=away_team, obj_in=away_team_update, db=db)
    crud_team.update(db_obj=home_team, obj_in=home_team_update, db=db)
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
