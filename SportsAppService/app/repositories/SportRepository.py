from SportsAppModels.models.Sport import (
    Sport,
    SportCreate,
    SportUpdate,
)

from app.repositories.BaseRepository import BaseRepository

class SportRepository(BaseRepository[
    Sport,
    SportCreate, 
    SportUpdate
]):
    default_relationships = ["sport_category"]  # Automatically load related categories

    def __init__(self):
        super().__init__(Sport)
