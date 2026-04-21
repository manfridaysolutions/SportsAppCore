from SportsAppModels.models.Athlete import (
    Athlete,
    AthleteCreate,
    AthleteUpdate,
    AthleteRead
)
from app.services.AthleteService import AthleteService
from app.api.v1.endpoints.BaseEndpoint import BaseEndpoint

athlete_service = AthleteService()

athlete_endpoint = BaseEndpoint[
    Athlete,
    AthleteCreate,
    AthleteUpdate,
    AthleteRead
](
    service=athlete_service,
    model_read=AthleteRead,
    prefix="/athlete",
    tags=["Athlete"]
).router
