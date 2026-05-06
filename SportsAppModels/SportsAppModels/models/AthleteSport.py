from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from .Athlete import Athlete
    from .Sport import Sport

class AthleteSportBase(SQLModel):
    athlete_id: int = Field(
        nullable=False,
        foreign_key="sports.athlete.athlete_id"
    )
    sport_id: int = Field(
        nullable=False,
        foreign_key="sports.sports.sport_id"
    )


class AthleteSport(AthleteSportBase, table=True):
    __tablename__ = "athlete_sports"
    __table_args__ = {"schema": "sports"}

    athlete_sport_id: Optional[int] = Field(default=None, primary_key=True)
    athlete_id: int = Field(foreign_key="sports.athletes.athlete_id")
    sport_id: int = Field(foreign_key="sports.sports.sport_id")
    # sys_period intentionally omitted (managed by PostgreSQL triggers)

    # --- Relationships ---
    athlete: Optional["Athlete"] = Relationship(back_populates="athlete_sports")
    sport: Optional[List["Sport"]] = Relationship(back_populates="athlete_sports")

class AthleteSportCreate(AthleteSportBase):
    athlete_sport_id: int


class AthleteSportRead(AthleteSportBase):
    athlete_id: int
    sport_id: int

class AthleteSportUpdate(AthleteSportBase):
    pass
    
from .Athlete import Athlete
from .Sport import Sport
AthleteSport.model_rebuild()
