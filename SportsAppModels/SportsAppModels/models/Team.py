from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .League import League
    from .Roster import Roster
    from .ReferenceValue import ReferenceValue
    from .Contract import Contract

class TeamBase(SQLModel):
    league_id: Optional[int] = Field(
        nullable=False,
        foreign_key="sports.leagues.league_id"
    )
    team_name: Optional[str] = Field(nullable=False, max_length=150)
    short_name: Optional[str] = Field(default=None, max_length=50)
    abbreviation: Optional[str] = Field(nullable=False, max_length=10)

    city_id: Optional[int] = Field(default=None,nullable=False, foreign_key="sports.reference_values.reference_value_id")
    state_province_id: Optional[int] = Field(default=None,nullable=False, foreign_key="sports.reference_values.reference_value_id")
    country_id: Optional[int] = Field(default=None,nullable=False, foreign_key="sports.reference_values.reference_value_id")
    venue_id: Optional[int] = Field(default=None,nullable=False, foreign_key="sports.reference_values.reference_value_id")

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

    # -- Relationships --
    rosters: Optional[List["Roster"]] = Relationship(
        back_populates="team",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    league: Optional["League"] = Relationship(back_populates="teams")
    
    city: Optional["ReferenceValue"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Team.city_id]"}
    )
    state_province: Optional["ReferenceValue"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Team.state_province_id]"}
    )
    country: Optional["ReferenceValue"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Team.country_id]"}
    )
    venue: Optional["ReferenceValue"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Team.venue_id]"}
    )

    contracts: Optional[List["Contract"]] = Relationship(
        back_populates="team",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class TeamCreate(TeamBase):
    # ensure fields are populated
    team_name: str
    abbreviation: str

class TeamRead(TeamBase):
    team_id: int

    # rosters: Optional[List["Roster"]] = None  # Include roster details in read model

    city: Optional["ReferenceValue"] = None
    state_province: Optional["ReferenceValue"] = None
    country: Optional["ReferenceValue"] = None
    venue: Optional["ReferenceValue"] = None

class TeamUpdate(TeamBase):
    pass

from .League import League
from .Roster import Roster
from .ReferenceValue import ReferenceValue
from .Contract import Contract

Team.model_rebuild()