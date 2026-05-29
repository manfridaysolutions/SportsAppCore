from datetime import date
from typing import TYPE_CHECKING, Optional, List

from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from .Roster import Roster
    from .AthleteSport import AthleteSport
    from .Contract import Contract
    from .ReferenceValue import ReferenceValue

class AthleteBase(SQLModel):
    first_name: Optional[str] = Field(default=None,nullable=False, max_length=100)
    last_name: Optional[str] = Field(default=None,nullable=False, max_length=100)
    display_name: Optional[str] = Field(default=None,nullable=False, max_length=200)

    birth_date: Optional[date] = None
    country_id: Optional[int] = Field(default=None,foreign_key="sports.reference_values.reference_value_id")

    height_inches: Optional[int] = None
    weight_lbs: Optional[int] = None

    is_active: Optional[bool] = Field(default=True)
    source_reference_id: Optional[str] = Field(default=None, max_length=100)


class Athlete(AthleteBase, table=True):
    __tablename__ = "athletes"
    __table_args__ = {"schema": "sports"}

    athlete_id: Optional[int] = Field(default=None, primary_key=True)

    # --- Relationships ---
    rosters: Optional[List["Roster"]] = Relationship(
        back_populates="athlete",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )  # Back reference to Roster
    athlete_sports: Optional[List["AthleteSport"]] = Relationship(
        back_populates="athlete", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    nationality: Optional["ReferenceValue"] = Relationship()
    contracts: Optional[List["Contract"]] = Relationship(
        back_populates="athlete",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class AthleteCreate(AthleteBase):
    athlete_sports: Optional[List[int]] = None
    first_name: str
    last_name: str
    display_name: str

class AthleteRead(AthleteBase):
    athlete_id: int

    rosters: Optional[List["Roster"]] = None  # Include roster details in read model
    athlete_sports: Optional[List["AthleteSport"]] = None
    nationality: Optional["ReferenceValue"] = None

class AthleteUpdate(AthleteBase):
    athlete_sports: Optional[List[int]] = None

from .Roster import Roster
from .AthleteSport import AthleteSport
from .Contract import Contract
from .ReferenceValue import ReferenceValue
Athlete.model_rebuild()