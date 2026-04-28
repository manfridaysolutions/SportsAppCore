from typing import TYPE_CHECKING, Optional, Dict, Any, List
from sqlmodel import Field, SQLModel, Relationship, Column, JSON

if TYPE_CHECKING:
    from .ReferenceCategory import ReferenceCategory
    from .Sport import Sport
    from .League import League

class ReferenceValueBase(SQLModel):
    reference_category_id: int = Field(
        foreign_key="sports.reference_categories.reference_category_id",
        nullable=False
    )
    value: str = Field(max_length=100, index=True)
    description: Optional[str] = Field(default=None)
    sort_order: Optional[int] = Field(default=None)
    metadata_field: Optional[Dict[str, Any]] = Field(
        default=None, 
        sa_column=Column("metadata", JSON)
    )

class ReferenceValue(ReferenceValueBase, table=True):
    __tablename__ = "reference_values"
    __table_args__ = {"schema": "sports"}

    reference_value_id: Optional[int] = Field(
        default=None, 
        primary_key=True,
        sa_column_kwargs={"autoincrement": True}
    )
    # --- Relationships ---    
    reference_category: Optional["ReferenceCategory"] = Relationship(back_populates="reference_values")
    sports: Optional[List["Sport"]]= Relationship(back_populates="sport_category")
    countries: Optional[List["League"]] = Relationship(back_populates="country") # Back reference to League for country

class ReferenceValueCreate(ReferenceValueBase):
    pass

class ReferenceValueRead(ReferenceValueBase):
    reference_value_id: int

    reference_category: Optional["ReferenceCategory"] = None  # Include category details in read model
    
    # sports: Optional[List["Sport"]] = None  # Include sport details in read model

class ReferenceValueUpdate(ReferenceValueBase):
    pass

from .ReferenceCategory import ReferenceCategory
from .Sport import Sport
from .League import League
ReferenceValue.model_rebuild()
