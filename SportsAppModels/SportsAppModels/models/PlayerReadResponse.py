from typing import List, Optional
from sqlmodel import SQLModel

from SportsAppModels.models.Athlete import AthleteRead
from SportsAppModels.models.Roster import RosterRead
from SportsAppModels.models.RosterPosition import RosterPositionRead

class PlayerReadResponse(SQLModel):
    athlete: AthleteRead
    roster: Optional[RosterRead] = None
    positions: List[RosterPositionRead] = []
