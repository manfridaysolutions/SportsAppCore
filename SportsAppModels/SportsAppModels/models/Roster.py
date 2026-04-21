from typing import Optional
from sqlmodel import SQLModel, Field


class RosterBase(SQLModel):
    athlete_id: int = Field(
        nullable=False,
        foreign_key="sports.athletes.athlete_id"
    )
    team_id: int = Field(
        nullable=False,
        foreign_key="sports.teams.team_id"
    )
    season_id: int = Field(
        nullable=False,
        foreign_key="sports.seasons.season_id"
    )

    is_primary_sport: bool = Field(default=True)
    status: str = Field(default="Active", max_length=50)
    jersey_number: Optional[str] = Field(default=None, max_length=10)


class Roster(RosterBase, table=True):
    __tablename__ = "rosters"
    __table_args__ = {"schema": "sports"}

    roster_id: Optional[int] = Field(default=None, primary_key=True)
    # sys_period intentionally omitted (managed by PostgreSQL triggers)


class RosterCreate(RosterBase):
    pass


class RosterRead(RosterBase):
    roster_id: int


class RosterUpdate(SQLModel):
    athlete_id: Optional[int] = None
    team_id: Optional[int] = None
    season_id: Optional[int] = None

    is_primary_sport: Optional[bool] = None
    status: Optional[str] = None
    jersey_number: Optional[str] = None
