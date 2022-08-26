# Copyright 2022 Marin Pejcin


from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from core.crud.crud_base import CRUDBase
from core.database.models.games import Game
from core.schemas.game import GameCreate, GameUpdate


class CRUDGame(CRUDBase[Game, GameCreate, GameUpdate]):
    def get_games_by_team(self, *, team_id: int, db: Session) -> List[Game]:
        return (
            db.query(self.model)
            .filter(
                or_(self.model.home_team == team_id, self.model.away_team == team_id)
            )
            .all()
        )


crud_game = CRUDGame(Game)
