from SportsAppModels.models.AthleteSport import (
    AthleteSport,
    AthleteSportCreate,
    AthleteSportUpdate,
)

from app.repositories.BaseRepository import BaseRepository

class AthleteSportRepository(BaseRepository[
    AthleteSport,
    AthleteSportCreate, 
    AthleteSportUpdate
]):
    
    def __init__(self):
        super().__init__(AthleteSport)
