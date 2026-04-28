from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .ReferenceValue import ReferenceValue, ReferenceValueRead

class ReferenceCategoryBase(SQLModel):
    name: str = Field(index=True, unique=True, max_length=100)
    description: Optional[str] = Field(default=None)

class ReferenceCategory(ReferenceCategoryBase, table=True):
    # Set the table name and explicit schema
    __tablename__ = "reference_categories"
    __table_args__ = {"schema": "sports"}

    # Define the primary key
    # sa_column_kwargs ensures the serial/identity column behavior is respected
    reference_category_id: Optional[int] = Field(
        default=None, 
        primary_key=True,
        sa_column_kwargs={"autoincrement": True}
    )

    # --- Relationships ---
    reference_values: List["ReferenceValue"] = Relationship(back_populates="reference_category")

class ReferenceCategoryCreate(ReferenceCategoryBase):
    pass

class ReferenceCategoryRead(ReferenceCategoryBase):
    reference_category_id: int

    reference_values: Optional[List["ReferenceValueRead"]] = None  # Include related values in read model

class ReferenceCategoryUpdate(ReferenceCategoryBase):
    pass

from .ReferenceValue import ReferenceValue, ReferenceValueRead
ReferenceCategory.model_rebuild()
ReferenceCategoryRead.model_rebuild()