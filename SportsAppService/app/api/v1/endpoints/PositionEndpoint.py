from SportsAppModels.models.Position import (
    Position,
    PositionCreate,
    PositionUpdate,
    PositionRead
)

from app.services.PositionService import PositionService
from app.api.v1.endpoints.BaseEndpoint import BaseEndpoint

position_service = PositionService()

position_endpoint = BaseEndpoint[
    Position,
    PositionCreate,
    PositionUpdate,
    PositionRead
](
    service=position_service,
    model_create=PositionCreate,
    model_read=PositionRead,
    model_update=PositionUpdate,
    prefix="/position",
    tags=["Position"]
).router
