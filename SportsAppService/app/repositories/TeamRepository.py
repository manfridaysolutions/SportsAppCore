from SportsAppModels.models.Team import (
    Team,
    TeamCreate,
    TeamUpdate,
)

from app.repositories.BaseRepository import BaseRepository

class TeamRepository(BaseRepository[
    Team,
    TeamCreate, 
    TeamUpdate
]):
    default_relationships = ["rosters", "city", "state_province", "country", "venue", "contracts"]  # Automatically load related categories
    
    def __init__(self):
        super().__init__(Team)
