# Copyright 2022 Marin Pejcin


from sqlalchemy import Column, Integer, String, DateTime, func

from core.database.database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    date_played = Column(DateTime(timezone=True), server_default=func.now())
    home_team = Column(Integer)
    home_goals = Column(Integer)
    away_team = Column(Integer)
    away_goals = Column(String)
