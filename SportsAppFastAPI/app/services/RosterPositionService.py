from SportsAppModels.models.RosterPosition import (
    RosterPosition,
    RosterPositionCreate,
    RosterPositionUpdate
)
from app.repositories.RosterPositionRepository import RosterPositionRepository
from app.services.BaseService import BaseService

class RosterPositionService(BaseService[RosterPosition, RosterPositionCreate, RosterPositionUpdate]):
    def __init__(self):
        super().__init__(RosterPositionRepository())