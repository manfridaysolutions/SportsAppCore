from typing import Optional
from sqlmodel import SQLModel, Field


class LeagueBase(SQLModel):
    league_name: str = Field(nullable=False, max_length=150)
    sport_id: int = Field(
        nullable=False,
        foreign_key="sports.sports.sport_id"
    )
    country: Optional[str] = Field(default=None, max_length=100)
    level: Optional[int] = Field(default=1)


class League(LeagueBase, table=True):
    __tablename__ = "leagues"
    __table_args__ = {"schema": "sports"}

    league_id: Optional[int] = Field(default=None, primary_key=True)

class LeagueCreate(LeagueBase):
    pass


class LeagueRead(LeagueBase):
    league_id: int

class LeagueUpdate(SQLModel):
    league_name: Optional[str] = None
    sport_id: Optional[int] = None
    country: Optional[str] = None
    level: Optional[int] = None
