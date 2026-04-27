from typing import TYPE_CHECKING, Optional
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from .RosterPosition import RosterPosition

class PositionBase(SQLModel):
    sport_id: int = Field(
        nullable=False,
        foreign_key="sports.sports.sport_id"
    )
    position_name: str = Field(nullable=False, max_length=100)
    position_abbreviation: str = Field(nullable=False, max_length=10)
    description: Optional[str] = None


class Position(PositionBase, table=True):
    __tablename__ = "positions"
    __table_args__ = {"schema": "sports"}

    position_id: Optional[int] = Field(default=None, primary_key=True)
    # sys_period intentionally omitted (managed by PostgreSQL triggers)

    # --- Relationships ---
    roster_positions: Optional[list["RosterPosition"]] = Relationship(back_populates="position")  # Back reference to RosterPosition

class PositionCreate(PositionBase):
    pass


class PositionRead(PositionBase):
    position_id: int

    roster_positions: Optional[list["RosterPosition"]] = None  # Include roster position details in read model

class PositionUpdate(PositionBase):
    pass

from .RosterPosition import RosterPosition
Position.model_rebuild()