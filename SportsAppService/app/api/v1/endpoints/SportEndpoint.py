from SportsAppModels.models.Sport import (
    Sport,
    SportCreate,
    SportUpdate,
    SportRead
)
from app.services.SportService import SportService
from app.api.v1.endpoints.BaseEndpoint import BaseEndpoint

sport_service = SportService()

sport_endpoint = BaseEndpoint[
    Sport,
    SportCreate,
    SportUpdate,
    SportRead
](
    service=sport_service,
    model_read=SportRead,
    model_update=SportUpdate,
    prefix="/sports",
    tags=["Sports"]
).router
