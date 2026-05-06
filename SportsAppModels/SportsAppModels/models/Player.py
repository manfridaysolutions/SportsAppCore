from typing import List, Optional
from datetime import date
from sqlmodel import SQLModel

from SportsAppModels.models.Athlete import AthleteCreate, AthleteRead, AthleteUpdate
from SportsAppModels.models.Roster import RosterCreate, RosterRead, RosterUpdate
from SportsAppModels.models.RosterPosition import RosterPositionCreate, RosterPositionRead, RosterPositionUpdate

class PlayerCreateRequest(SQLModel):
    athlete: AthleteCreate
    roster: RosterCreate
    roster_positions: List[RosterPositionCreate] = []

class PlayerReadResponse(SQLModel):
    athlete: AthleteRead
    roster: Optional[RosterRead] = None
    roster_positions: List[RosterPositionRead] = []

class PlayerUpdateRequest(SQLModel):
    athlete: Optional[AthleteUpdate] = None
    roster: Optional[RosterUpdate] = None
    roster_positions: Optional[List[RosterPositionUpdate]] = None

class PlayerTradeRequest(SQLModel):
    new_roster: RosterCreate
    new_roster_positions: List[RosterPositionCreate] = []
