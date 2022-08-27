# Copyright 2022 Marin Pejcin


from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.database.database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    team_name = Column(String, unique=True)
    # games_played = Column(Integer)
    wins = Column(Integer)
    draws = Column(Integer)
    losses = Column(Integer)
    goals_for = Column(Integer)
    goals_against = Column(Integer)
    # points = Column(Integer)

    players = relationship("Player", back_populates="team")
