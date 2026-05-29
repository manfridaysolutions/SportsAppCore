from SportsAppModels.models.RosterPosition import (
    RosterPosition,
    RosterPositionCreate,
    RosterPositionRead,
    RosterPositionUpdate
)

from app.services.RosterPositionService import RosterPositionService
from app.api.v1.endpoints.BaseEndpoint import BaseEndpoint

roster_position_service = RosterPositionService()

roster_position_endpoint = BaseEndpoint[
    RosterPosition,
    RosterPositionCreate,
    RosterPositionRead,
    RosterPositionUpdate
](
    service=roster_position_service,
    model_create=RosterPositionCreate,
    model_read=RosterPositionRead,
    model_update=RosterPositionUpdate,
    prefix="/roster_positions",
    tags=["Roster Positions"]
).router