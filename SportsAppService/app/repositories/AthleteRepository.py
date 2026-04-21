from SportsAppModels.models.Athlete import (
    Athlete,
    AthleteCreate,
    AthleteUpdate,
)

from app.repositories.BaseRepository import BaseRepository

class AthleteRepository(BaseRepository[
    Athlete,
    AthleteCreate, 
    AthleteUpdate
]):
    def __init__(self):
        super().__init__(Athlete)
