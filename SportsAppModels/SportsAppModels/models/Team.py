from typing import Optional
from sqlmodel import SQLModel, Field


class TeamBase(SQLModel):
    league_id: int = Field(
        nullable=False,
        foreign_key="sports.leagues.league_id"
    )
    team_name: str = Field(nullable=False, max_length=150)
    short_name: Optional[str] = Field(default=None, max_length=50)
    abbreviation: str = Field(nullable=False, max_length=10)

    city: Optional[str] = Field(default=None, max_length=100)
    state_province: Optional[str] = Field(default=None, max_length=100)
    country: Optional[str] = Field(default=None, max_length=100)

    venue_name: Optional[str] = Field(default=None, max_length=200)

    primary_color: Optional[str] = Field(default=None, max_length=7)
    secondary_color: Optional[str] = Field(default=None, max_length=7)

    logo_url: Optional[str] = None
    founded_year: Optional[int] = None

    is_active: Optional[bool] = Field(default=True)


class Team(TeamBase, table=True):
    __tablename__ = "teams"
    __table_args__ = {"schema": "sports"}

    team_id: Optional[int] = Field(default=None, primary_key=True)
    # sys_period intentionally omitted (managed by PostgreSQL triggers)


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    team_id: int


class TeamUpdate(SQLModel):
    league_id: Optional[int] = None
    team_name: Optional[str] = None
    short_name: Optional[str] = None
    abbreviation: Optional[str] = None

    city: Optional[str] = None
    state_province: Optional[str] = None
    country: Optional[str] = None

    venue_name: Optional[str] = None

    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None

    logo_url: Optional[str] = None
    founded_year: Optional[int] = None

    is_active: Optional[bool] = None
