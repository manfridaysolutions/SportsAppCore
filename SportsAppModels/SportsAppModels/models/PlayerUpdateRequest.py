from typing import List, Optional
from sqlmodel import SQLModel

from SportsAppModels.models.Athlete import AthleteUpdate
from SportsAppModels.models.Roster import RosterUpdate
from SportsAppModels.models.RosterPosition import RosterPositionCreate, RosterPositionUpdate


class PlayerUpdateRequest(SQLModel):
    athlete: Optional[AthleteUpdate] = None
    roster: Optional[RosterUpdate] = None
    positions: Optional[List[RosterPositionCreate]] = None
