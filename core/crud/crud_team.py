# Copyright 2022 Marin Pejcin


from sqlalchemy.orm import Session

from core.crud.crud_base import CRUDBase
from core.database.models.teams import Team
from core.schemas.team import TeamCreate, TeamUpdate


class CRUDTeam(CRUDBase[Team, TeamCreate, TeamUpdate]):
    def get_by_team_name(self, *, team_name: str, db: Session) -> Team:
        return db.query(self.model).filter(self.model.team_name == team_name).first()


crud_team = CRUDTeam(Team)
