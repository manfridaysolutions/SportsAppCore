from datetime import datetime
from typing import TYPE_CHECKING, Optional, List

from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from .ReferenceValue import ReferenceValue
    from .AthleteSport import AthleteSport

class SportBase(SQLModel):
    sport_name: Optional[str] = Field(default=None,nullable=False, max_length=100, index=True)
    category_id: Optional[int] = Field(default=None,nullable=False, foreign_key="sports.reference_values.reference_value_id")
    is_team_sport: Optional[bool] = Field(default=False)
    governing_body: Optional[str] = Field(default=None,max_length=100)
    description: Optional[str] = None

class Sport(SportBase, table=True):
    __tablename__ = "sports"
    __table_args__ = {"schema": "sports"}

    sport_id: Optional[int] = Field(default=None, primary_key=True)
    
    # Keep the relationship here, not in the Base class, to avoid circular imports
    sport_category: Optional["ReferenceValue"] = Relationship() # Back reference to ReferenceValue for sport_category   
    athlete_sports: Optional[List["AthleteSport"]] = Relationship(back_populates="sport")

class SportCreate(SportBase):
    sport_name: str
    category_id: int

class SportRead(SportBase):
    sport_id: int

    sport_category: Optional["ReferenceValue"] = None  # Include category details in read model

class SportUpdate(SportBase):
    pass

from.ReferenceValue import ReferenceValue
Sport.model_rebuild()