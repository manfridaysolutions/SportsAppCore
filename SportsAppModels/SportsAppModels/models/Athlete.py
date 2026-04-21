from datetime import date
from typing import Optional

from sqlmodel import SQLModel, Field


class AthleteBase(SQLModel):
    first_name: str = Field(nullable=False, max_length=100)
    last_name: str = Field(nullable=False, max_length=100)
    display_name: str = Field(nullable=False, max_length=200)

    birth_date: Optional[date] = None
    country_id: Optional[int] = None

    height_inches: Optional[int] = None
    weight_lbs: Optional[int] = None

    is_active: bool = Field(default=True)
    source_reference_id: Optional[str] = Field(default=None, max_length=100)


class Athlete(AthleteBase, table=True):
    __tablename__ = "athletes"
    __table_args__ = {"schema": "sports"}

    athlete_id: Optional[int] = Field(default=None, primary_key=True)


class AthleteCreate(AthleteBase):
    pass


class AthleteRead(AthleteBase):
    athlete_id: int

class AthleteUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None

    birth_date: Optional[date] = None
    country_id: Optional[int] = None

    height_inches: Optional[int] = None
    weight_lbs: Optional[int] = None

    is_active: Optional[bool] = None
    source_reference_id: Optional[str] = None
