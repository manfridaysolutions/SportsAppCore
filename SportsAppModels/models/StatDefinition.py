from typing import TYPE_CHECKING, Optional
from sqlalchemy import null
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from .ReferenceValue import ReferenceValue

class StatDefinitionBase(SQLModel):
    stat_name: Optional[str] = Field(default=None,nullable=False, max_length=150)
    sport_id: Optional[int] = Field(default=None,nullable=False, foreign_key="sports.sports.sport_id")
    stat_unit_id: Optional[int] = Field(default=None,foreign_key="sports.reference_values.reference_value_id")
    stat_abbreviation: Optional[str] = Field(default=None,nullable=False, max_length=20)

class StatDefinition(StatDefinitionBase, table=True):
    __tablename__ = "stat_definitions"
    __table_args__ = {"schema": "sports"}

    stat_def_id: Optional[int] = Field(default=None, primary_key=True)

    # --- Relationships ---
    stat_unit: Optional["ReferenceValue"] = Relationship() # Back reference to ReferenceValue for country

class StatDefinitionCreate(StatDefinitionBase):
    sport_id: int
    stat_name: str
    stat_abbreviation: str

class StatDefinitionRead(StatDefinitionBase):
    stat_def_id: int

    stat_unit: Optional["ReferenceValue"] = None  # Include country details in read model

class StatDefinitionUpdate(StatDefinitionBase):
    pass

from .ReferenceValue import ReferenceValue
StatDefinition.model_rebuild()