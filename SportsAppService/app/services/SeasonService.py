from SportsAppModels.models.Season import (
    Season,
    SeasonCreate,
    SeasonUpdate,
)
from app.repositories.SeasonRepository import SeasonRepository
from app.services.BaseService import BaseService

class SeasonService(BaseService[Season, SeasonCreate, SeasonUpdate]):
    def __init__(self):
        super().__init__(SeasonRepository())