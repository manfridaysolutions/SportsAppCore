from typing import List, Optional
from datetime import date
from sqlmodel import SQLModel

from SportsAppModels.models.Athlete import AthleteCreate
from SportsAppModels.models.Roster import RosterCreate
from SportsAppModels.models.RosterPosition import RosterPositionCreate


class PlayerCreateRequest(SQLModel):
    athlete: AthleteCreate
    roster: RosterCreate
    positions: List[RosterPositionCreate] = []
