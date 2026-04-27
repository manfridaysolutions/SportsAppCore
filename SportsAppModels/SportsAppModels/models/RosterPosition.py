from turtle import position
from typing import TYPE_CHECKING, Optional
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from .Position import Position
    from .Roster import Roster

class RosterPositionBase(SQLModel):
    roster_id: int = Field(
        nullable=False,
        foreign_key="sports.rosters.roster_id"
    )
    position_id: int = Field(
        nullable=False,
        foreign_key="sports.positions.position_id"
    )

    is_starting_role: Optional[bool] = Field(default=False)
    snap_count_percentage: Optional[int] = None


class RosterPosition(RosterPositionBase, table=True):
    __tablename__ = "roster_positions"
    __table_args__ = {"schema": "sports"}

    # Composite primary key
    roster_id: int = Field(
        primary_key=True,
        foreign_key="sports.rosters.roster_id"
    )
    position_id: int = Field(
        primary_key=True,
        foreign_key="sports.positions.position_id"
    )
    # sys_period intentionally omitted (managed by PostgreSQL triggers)

    # --- Relationships ---
    position: Optional["Position"] = Relationship(back_populates="roster_positions")
    roster: Optional["Roster"] = Relationship(back_populates="roster_positions")

class RosterPositionCreate(RosterPositionBase):
    pass


class RosterPositionRead(RosterPositionBase):
    roster_id: int
    position_id: int

    position: Optional["Position"] = None  # Include position details in read model
    # roster: Optional["Roster"] = None  # Include roster details in read model

class RosterPositionUpdate(SQLModel):
    is_starting_role: Optional[bool] = None
    snap_count_percentage: Optional[int] = None

from .Position import Position
from .Roster import Roster
RosterPosition.model_rebuild()
