from typing import Optional
from sqlmodel import SQLModel, Field


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


class PositionCreate(PositionBase):
    pass


class PositionRead(PositionBase):
    position_id: int


class PositionUpdate(SQLModel):
    sport_id: Optional[int] = None
    position_name: Optional[str] = None
    position_abbreviation: Optional[str] = None
    description: Optional[str] = None
