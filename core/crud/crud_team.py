# Copyright 2022 Marin Pejcin


from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session

from core.crud.crud_base import CRUDBase
from core.database.models.teams import Team
from core.schemas.game import GameCreate
from core.schemas.team import TeamCreate, TeamUpdate


class CRUDTeam(CRUDBase[Team, TeamCreate, TeamUpdate]):
    def get_by_team_name(self, *, team_name: str, db: Session) -> Team:
        return (
            db.query(self.model)
            .filter(func.lower(self.model.team_name) == team_name.lower())
            .first()
        )

    def update_stats(
        self, *, home_team: Team, away_team: Team, game_in: GameCreate, db: Session
    ) -> List[Team]:
        db.query(Team).filter(Team.id == home_team.id).update(
            {
                "goals_for": home_team.goals_for + game_in.home_goals,
                "goals_against": home_team.goals_against + game_in.away_goals,
            }
        )
        db.query(Team).filter(Team.id == away_team.id).update(
            {
                "goals_for": away_team.goals_for + game_in.away_goals,
                "goals_against": away_team.goals_against + game_in.home_goals,
            }
        )
        if game_in.home_goals > game_in.away_goals:
            db.query(Team).filter(Team.id == home_team.id).update(
                {"wins": home_team.wins + 1}
            )
            db.query(Team).filter(Team.id == away_team.id).update(
                {"losses": away_team.losses + 1}
            )
        if game_in.home_goals < game_in.away_goals:
            db.query(Team).filter(Team.id == home_team.id).update(
                {"losses": home_team.losses + 1}
            )
            db.query(Team).filter(Team.id == away_team.id).update(
                {"wins": away_team.wins + 1}
            )
        if game_in.home_goals == game_in.away_goals:
            db.query(Team).filter(Team.id == home_team.id).update(
                {"draws": home_team.draws + 1}
            )
            db.query(Team).filter(Team.id == away_team.id).update(
                {"draws": away_team.draws + 1}
            )
        db.commit()


crud_team = CRUDTeam(Team)
