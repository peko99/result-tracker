# Copyright 2022 Marin Pejcin


from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.crud import crud_player
from dependencies import get_db
from core.schemas import Player, PlayerCreate, PlayerUpdate


router = APIRouter(
    prefix='/player',
    tags=['player'],
    dependencies=[Depends(get_db)]
)


@router.post('', response_model=Player)
async def create_player(
    player_in: PlayerCreate,
    db: Session = Depends(get_db)
) -> Any:
    try:
        created_player = crud_player.create(obj_in=player_in, db=db)
    except IntegrityError as error:
        db.rollback()
        raise Exception(error)
    else:
        return created_player


@router.get('', response_model=List[Player])
async def get_players(
    db: Session = Depends(get_db)
) -> Any:
    return crud_player.get_all(db=db)


@router.delete('/{id_}', response_model=Player)
async def delete_player(
    id_: int,
    db: Session = Depends(get_db)
) -> Any:
    player = crud_player.get(id_=id_, db=db)
    if not player:
        raise Exception('player not found!')
    
    return crud_player.delete(id_=id_, db=db)
