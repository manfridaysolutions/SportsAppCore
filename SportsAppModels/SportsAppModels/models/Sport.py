from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class SportBase(SQLModel):
    sport_name: str = Field(nullable=False, max_length=100, index=True)
    category_id: int = Field(nullable=False, foreign_key="sports.sport_categories.category_id")
    is_team_sport: bool = Field(default=False)
    governing_body: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None


class Sport(SportBase, table=True):
    __tablename__ = "sports"
    __table_args__ = {"schema": "sports"}

    sport_id: Optional[int] = Field(default=None, primary_key=True)

class SportCreate(SportBase):
    pass


class SportRead(SportBase):
    sport_id: int

class SportUpdate(SQLModel):
    sport_name: Optional[str] = None
    category_id: Optional[int] = None
    is_team_sport: Optional[bool] = None
    governing_body: Optional[str] = None
    description: Optional[str] = None
