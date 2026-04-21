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
    def __init__(self):
        super().__init__(Sport)
