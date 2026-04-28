from typing import TYPE_CHECKING, Optional
from sqlalchemy import null
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from .ReferenceValue import ReferenceValue

class LeagueBase(SQLModel):
    league_name: str = Field(nullable=False, max_length=150)
    sport_id: int = Field(
        nullable=False,
        foreign_key="sports.sports.sport_id"
    )
    country_id: Optional[int] = Field(default=None,foreign_key="sports.reference_values.reference_value_id")
    level: Optional[int] = Field(default=1)

class League(LeagueBase, table=True):
    __tablename__ = "leagues"
    __table_args__ = {"schema": "sports"}

    league_id: Optional[int] = Field(default=None, primary_key=True)

    # --- Relationships ---
    country: Optional["ReferenceValue"] = Relationship(back_populates="countries") # Back reference to ReferenceValue for country

class LeagueCreate(LeagueBase):
    pass

class LeagueRead(LeagueBase):
    league_id: int

    country: Optional["ReferenceValue"] = None  # Include country details in read model

class LeagueUpdate(SQLModel):
    league_name: Optional[str] = None
    sport_id: Optional[int] = None
    country_id: Optional[int] = None
    level: Optional[int] = None

from .ReferenceValue import ReferenceValue
League.model_rebuild()