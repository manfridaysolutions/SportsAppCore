from SportsAppModels.models.Team import (
    Team,
    TeamCreate,
    TeamUpdate,
    TeamRead
)

from app.services.TeamService import TeamService
from app.api.v1.endpoints.BaseEndpoint import BaseEndpoint

team_service = TeamService()

team_endpoint = BaseEndpoint[
    Team,
    TeamCreate,
    TeamUpdate,
    TeamRead
](
    service=team_service,
    model_read=TeamRead,
    model_update=TeamUpdate,
    prefix="/team",
    tags=["Team"]
).router
