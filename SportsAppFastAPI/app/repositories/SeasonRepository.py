from SportsAppModels.models.Season import (
    Season,
    SeasonCreate,
    SeasonUpdate,
)

from app.repositories.BaseRepository import BaseRepository

class SeasonRepository(BaseRepository[
    Season,
    SeasonCreate, 
    SeasonUpdate
]):
    default_relationships = ["league"]  # Automatically load related categories
    
    def __init__(self):
        super().__init__(Season)
