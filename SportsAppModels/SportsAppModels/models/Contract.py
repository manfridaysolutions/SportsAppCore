from datetime import date
from typing import TYPE_CHECKING, Optional, Any, Dict
from decimal import Decimal
from sqlalchemy import Column, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from .Athlete import Athlete
    from .Team import Team
    from .Season import Season
    from .ReferenceValue import ReferenceValue

class ContractBase(SQLModel):
    athlete_id: Optional[int] = Field(default=None, foreign_key="sports.athletes.athlete_id")
    team_id: Optional[int] = Field(default=None, foreign_key="sports.teams.team_id")
    start_season_id: Optional[int] = Field(default=None, foreign_key="sports.seasons.season_id")
    end_season_id: Optional[int] = Field(default=None, foreign_key="sports.seasons.season_id")
    
    signed_date: Optional[date] = Field(default_factory=date.today)
    
    # Using sa_column to ensure precision matches your Numeric(14, 2)
    total_value: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(14, 2)))
    guaranteed_amount: Optional[Decimal] = Field(default=None, sa_column=Column(Numeric(14, 2)))
    
    # JSONB for the GIN index
    details: Optional[Dict[str, Any]] = Field(default_factory=dict, sa_column=Column(JSONB))
    
    contract_type_id: Optional[int] = Field(default=None, foreign_key="sports.reference_values.reference_value_id")
    is_active: Optional[bool] = Field(default=True)

class Contract(ContractBase, table=True):
    __tablename__ = "contracts"
    __table_args__ = {"schema": "sports"}

    contract_id: Optional[int] = Field(default=None, primary_key=True)

    # --- Relationships ---
    athlete: Optional["Athlete"] = Relationship(back_populates="contracts")
    team: Optional["Team"] = Relationship(back_populates="contracts")
    start_season: Optional["Season"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Contract.start_season_id]"}
    )
    end_season: Optional["Season"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Contract.end_season_id]"}
    )
    contract_type: Optional["ReferenceValue"] = Relationship()

class ContractCreate(ContractBase):
    athlete_id: int
    team_id: int

class ContractRead(ContractBase):
    contract_id: int

    athlete: Optional["Athlete"] = None;
    team: Optional["Team"] = None;
    start_season: Optional["Season"] = None;
    end_season: Optional["Season"] = None;
    contract_type: Optional["ReferenceValue"] = None;

class ContractUpdate(ContractBase):
    pass

from .Athlete import Athlete
from .Team import Team
from .Season import Season
from .ReferenceValue import ReferenceValue
Contract.model_rebuild()