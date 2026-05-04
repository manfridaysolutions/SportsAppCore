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
    default_relationships = ["country"]  # Automatically load related categories

    def __init__(self):
        super().__init__(League)