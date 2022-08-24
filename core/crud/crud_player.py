# Copyright 2022 Marin Pejcin


from sqlalchemy.orm import Session

from core.crud.crud_base import CRUDBase
from core.database.models.players import Player
from core.schemas.player import PlayerCreate, PlayerUpdate


class CRUDPlayer(CRUDBase[Player, PlayerCreate, PlayerUpdate]):
    def get_by_username(self, *, username: str, db: Session) -> Player:
        return db.query(self.model).filter(self.model.username == username).first()


crud_player = CRUDPlayer(Player)
