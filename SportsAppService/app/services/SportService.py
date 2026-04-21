from SportsAppModels.models.Sport import (
    Sport,
    SportCreate,
    SportUpdate,
)
from app.repositories.SportRepository import SportRepository
from app.services.BaseService import BaseService

class SportService(BaseService[Sport, SportCreate, SportUpdate]):
    def __init__(self):
        super().__init__(SportRepository())