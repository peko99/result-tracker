# Copyright 2022 Marin Pejcin


from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.crud import crud_team
from dependencies import get_db
from core.schemas import Team, TeamCreate, TeamUpdate


router = APIRouter(
    prefix='/team',
    tags=['team'],
    dependencies=[Depends(get_db)]
)


@router.post('', response_model=Team)
async def create_team(
    team_in: TeamCreate,
    db: Session = Depends(get_db)
) -> Any:
    try:
        created_team = crud_team.create(obj_in=team_in, db=db)
    except IntegrityError as error:
        db.rollback()
        raise Exception(error)
    else:
        return created_team


@router.get('', response_model=List[Team])
async def get_teams(
    db: Session = Depends(get_db)
) -> Any:
    return crud_team.get_all(db=db)


@router.delete('/{id_}', response_model=Team)
async def delete_team(
    id_: int,
    db: Session = Depends(get_db)
) -> Any:
    team = crud_team.get(id_=id_, db=db)
    if not team:
        raise Exception('team not found!')
    
    return crud_team.delete(id_=id_, db=db)
