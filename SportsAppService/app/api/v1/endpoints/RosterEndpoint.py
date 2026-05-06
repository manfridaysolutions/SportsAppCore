from SportsAppModels.models.Roster import (
    Roster,
    RosterCreate,
    RosterUpdate,
    RosterRead
)

from app.services.RosterService import RosterService
from app.api.v1.endpoints.BaseEndpoint import BaseEndpoint

roster_service = RosterService()

roster_endpoint = BaseEndpoint[
    Roster,
    RosterCreate,
    RosterUpdate,
    RosterRead
](
    service=roster_service,
    model_create=RosterCreate,
    model_read=RosterRead,
    model_update=RosterUpdate,
    prefix="/roster",
    tags=["Roster"]
).router
