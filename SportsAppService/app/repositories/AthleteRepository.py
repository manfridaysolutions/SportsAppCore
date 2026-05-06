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
    default_relationships = ["rosters", "athlete_sports", "nationality"]  # Automatically load related categories
    
    def __init__(self):
        super().__init__(Athlete)
