# Copyright 2022 Marin Pejcin


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.database.database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    team_id = Column(Integer, ForeignKey("teams.id"))

    team = relationship("Team", back_populates="players")
