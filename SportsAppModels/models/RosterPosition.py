from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from .Position import Position
    from .Roster import Roster

class RosterPositionBase(SQLModel):
    roster_id: Optional[int] = Field(
        default=None,
        nullable=False,
        foreign_key="sports.rosters.roster_id"
    )
    position_id: Optional[int] = Field(
        default=None,
        nullable=False,
        foreign_key="sports.positions.position_id"
    )

    is_starting_role: Optional[bool] = Field(default=False)
    snap_count_percentage: Optional[int] = None


class RosterPosition(RosterPositionBase, table=True):
    __tablename__ = "roster_positions"
    __table_args__ = {"schema": "sports"}

    roster_position_id: Optional[int] = Field(default=None, primary_key=True)

    # --- Relationships ---
    position: Optional["Position"] = Relationship(back_populates="roster_positions")
    roster: Optional["Roster"] = Relationship(back_populates="roster_positions")

class RosterPositionCreate(RosterPositionBase):
    roster_positions: Optional[List[int]] = None

class RosterPositionRead(RosterPositionBase):
    roster_position_id: int

    position: Optional["Position"] = None  # Include position details in read model
    # roster: Optional["Roster"] = None  # Include roster details in read model

class RosterPositionUpdate(RosterPositionBase):
    pass

from .Position import Position
from .Roster import Roster
RosterPosition.model_rebuild()
