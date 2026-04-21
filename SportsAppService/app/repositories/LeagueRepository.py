from SportsAppModels.models.League import (
    League,
    LeagueCreate,
    LeagueUpdate,
)

from app.repositories.BaseRepository import BaseRepository

class LeagueRepository(BaseRepository[
    League,
    LeagueCreate, 
    LeagueUpdate
]):
    def __init__(self):
        super().__init__(League)
