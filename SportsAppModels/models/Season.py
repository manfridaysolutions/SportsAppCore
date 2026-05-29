from datetime import date
from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .League import League

class SeasonBase(SQLModel):
    league_id: Optional[int] = Field(
        nullable=False,
        foreign_key="sports.leagues.league_id"
    )
    season_year: Optional[str] = Field(nullable=False, max_length=20)
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    is_active: Optional[bool] = Field(default=False)


class Season(SeasonBase, table=True):
    __tablename__ = "seasons"
    __table_args__ = {"schema": "sports"}

    season_id: Optional[int] = Field(default=None, primary_key=True)
    # sys_period intentionally omitted (managed by PostgreSQL triggers)

    # --- Relationships ---
    league: Optional["League"] = Relationship(back_populates="seasons")

class SeasonCreate(SeasonBase):
    league_id: str
    season_year: str


class SeasonRead(SeasonBase):
    season_id: int

    league: Optional["League"] = None;

class SeasonUpdate(SQLModel):
    pass

from .League import League
Season.model_rebuild()