from SportsAppModels.models.Roster import (
    Roster,
    RosterCreate,
    RosterUpdate,
)
from app.repositories.RosterRepository import RosterRepository
from app.services.BaseService import BaseService

class RosterService(BaseService[Roster, RosterCreate, RosterUpdate]):
    def __init__(self):
        super().__init__(RosterRepository())