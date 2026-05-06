from SportsAppModels.models.Season import (
    Season,
    SeasonCreate,
    SeasonUpdate,
    SeasonRead
)

from app.services.SeasonService import SeasonService
from app.api.v1.endpoints.BaseEndpoint import BaseEndpoint

season_service = SeasonService()

season_endpoint = BaseEndpoint[
    Season,
    SeasonCreate,
    SeasonUpdate,
    SeasonRead
](
    service=season_service,
    model_create=SeasonCreate,
    model_read=SeasonRead,
    model_update=SeasonUpdate,
    prefix="/season",
    tags=["Season"]
).router
