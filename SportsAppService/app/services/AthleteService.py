from SportsAppModels.models.Athlete import (
    Athlete,
    AthleteCreate,
    AthleteUpdate,
)
from app.repositories.AthleteRepository import AthleteRepository
from app.services.BaseService import BaseService

class AthleteService(BaseService[Athlete, AthleteCreate, AthleteUpdate]):
    def __init__(self):
        super().__init__(AthleteRepository())