from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field


class SeasonBase(SQLModel):
    league_id: int = Field(
        nullable=False,
        foreign_key="sports.leagues.league_id"
    )
    season_year: str = Field(nullable=False, max_length=20)

    start_date: Optional[date] = None
    end_date: Optional[date] = None

    is_active: bool = Field(default=False)


class Season(SeasonBase, table=True):
    __tablename__ = "seasons"
    __table_args__ = {"schema": "sports"}

    season_id: Optional[int] = Field(default=None, primary_key=True)
    # sys_period intentionally omitted (managed by PostgreSQL triggers)


class SeasonCreate(SeasonBase):
    pass


class SeasonRead(SeasonBase):
    season_id: int


class SeasonUpdate(SQLModel):
    league_id: Optional[int] = None
    season_year: Optional[str] = None

    start_date: Optional[date] = None
    end_date: Optional[date] = None

    is_active: Optional[bool] = None
