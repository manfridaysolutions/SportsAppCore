from typing import TYPE_CHECKING, Optional
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from .RosterPosition import RosterPosition

class PositionBase(SQLModel):
    sport_id: Optional[int] = Field(
        default=None,
        nullable=False,
        foreign_key="sports.sports.sport_id"
    )
    position_name: Optional[str] = Field(default=None,nullable=False, max_length=100)
    position_abbreviation: Optional[str] = Field(default=None,nullable=False, max_length=10)
    description: Optional[str] = None


class Position(PositionBase, table=True):
    __tablename__ = "positions"
    __table_args__ = {"schema": "sports"}

    position_id: Optional[int] = Field(default=None, primary_key=True)
    # sys_period intentionally omitted (managed by PostgreSQL triggers)

    # --- Relationships ---
    roster_positions: Optional[list["RosterPosition"]] = Relationship(
        back_populates="position",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class PositionCreate(PositionBase):
    position_name: str
    position_abbreviation: str    

class PositionRead(PositionBase):
    position_id: int

    # roster_positions: Optional[list["RosterPosition"]] = None  # Include roster position details in read model

class PositionUpdate(PositionBase):
    pass

from .RosterPosition import RosterPosition
Position.model_rebuild()