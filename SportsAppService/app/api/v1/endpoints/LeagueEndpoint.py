from SportsAppModels.models.League import (
    League,
    LeagueCreate,
    LeagueUpdate,
    LeagueRead
)

from app.services.LeagueService import LeagueService
from app.api.v1.endpoints.BaseEndpoint import BaseEndpoint

league_service = LeagueService()

league_endpoint = BaseEndpoint[
    League,
    LeagueCreate,
    LeagueUpdate,
    LeagueRead
](
    service=league_service,
    model_read=LeagueRead,
    prefix="/league",
    tags=["League"]
).router
