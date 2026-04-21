from typing import Optional
from sqlmodel import SQLModel, Field


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


class RosterPositionCreate(RosterPositionBase):
    pass


class RosterPositionRead(RosterPositionBase):
    roster_id: int
    position_id: int


class RosterPositionUpdate(SQLModel):
    is_starting_role: Optional[bool] = None
    snap_count_percentage: Optional[int] = None
