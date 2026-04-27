from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from .Roster import Roster

class AthleteBase(SQLModel):
    first_name: str = Field(nullable=False, max_length=100)
    last_name: str = Field(nullable=False, max_length=100)
    display_name: str = Field(nullable=False, max_length=200)

    birth_date: Optional[date] = None
    country_id: Optional[int] = None

    height_inches: Optional[int] = None
    weight_lbs: Optional[int] = None

    is_active: bool = Field(default=True)
    source_reference_id: Optional[str] = Field(default=None, max_length=100)


class Athlete(AthleteBase, table=True):
    __tablename__ = "athletes"
    __table_args__ = {"schema": "sports"}

    athlete_id: Optional[int] = Field(default=None, primary_key=True)

    # --- Relationships ---
    rosters: Optional[list["Roster"]] = Relationship(back_populates="athlete")  # Back reference to Roster


class AthleteCreate(AthleteBase):
    pass


class AthleteRead(AthleteBase):
    athlete_id: int

    rosters: Optional[list["Roster"]] = None  # Include roster details in read model

class AthleteUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None

    birth_date: Optional[date] = None
    country_id: Optional[int] = None

    height_inches: Optional[int] = None
    weight_lbs: Optional[int] = None

    is_active: Optional[bool] = None
    source_reference_id: Optional[str] = None

from .Roster import Roster
Athlete.model_rebuild()