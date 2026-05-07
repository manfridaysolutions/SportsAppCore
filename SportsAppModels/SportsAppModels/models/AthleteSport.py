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

    athlete_id: int = Field(foreign_key="sports.athletes.athlete_id", primary_key=True)
    sport_id: int = Field(foreign_key="sports.sports.sport_id", primary_key=True)
    # sys_period intentionally omitted (managed by PostgreSQL triggers)

    # --- Relationships ---
    athlete: Optional["Athlete"] = Relationship(back_populates="athlete_sports")
    sport: Optional[List["Sport"]] = Relationship(back_populates="athlete_sports")

class AthleteSportCreate(AthleteSportBase):
    pass

class AthleteSportRead(AthleteSportBase):
    pass

class AthleteSportUpdate(AthleteSportBase):
    pass
    
from .Athlete import Athlete
from .Sport import Sport
AthleteSport.model_rebuild()
