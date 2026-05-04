from typing import TYPE_CHECKING, Optional
from sqlalchemy import null
from sqlmodel import Relationship, SQLModel, Field
from pydantic import field_validator

if TYPE_CHECKING:
    from .ReferenceValue import ReferenceValue

class LeagueBase(SQLModel):
    league_name: Optional[str] = Field(default=None,nullable=False, max_length=150)
    sport_id: Optional[int] = Field(
        default=None,
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
    country: Optional["ReferenceValue"] = Relationship() # Back reference to ReferenceValue for country

class LeagueCreate(LeagueBase):
    league_name: str  # No default = Required
    sport_id: int     # No default = Required

class LeagueRead(LeagueBase):
    league_id: int
    country: Optional["ReferenceValue"] = None  # Include country details in read model

class LeagueUpdate(LeagueBase):
    @field_validator("league_name")
    @classmethod
    def name_must_not_be_empty(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError("League name cannot be empty")
        return v

    @field_validator("sport_id")
    @classmethod
    def sport_must_be_valid(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Invalid sport ID")
        return v
    
    @field_validator("country_id")
    @classmethod
    def country_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Selected country ID is invalid")
        return v
    
from .ReferenceValue import ReferenceValue
League.model_rebuild()