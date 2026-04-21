from SportsAppModels.models.League import (
    League,
    LeagueCreate,
    LeagueUpdate,
)
from app.repositories.LeagueRepository import LeagueRepository
from app.services.BaseService import BaseService

class LeagueService(BaseService[League, LeagueCreate, LeagueUpdate]):
    def __init__(self):
        super().__init__(LeagueRepository())