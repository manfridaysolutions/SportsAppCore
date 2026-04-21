from typing import List
from sqlmodel import SQLModel

from SportsAppModels.models.Roster import RosterCreate
from SportsAppModels.models.RosterPosition import RosterPositionCreate

class PlayerTradeRequest(SQLModel):
    new_roster: RosterCreate
    new_positions: List[RosterPositionCreate] = []
