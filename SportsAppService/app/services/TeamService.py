from SportsAppModels.models.Team import (
    Team,
    TeamCreate,
    TeamUpdate,
)
from app.repositories.TeamRepository import TeamRepository
from app.services.BaseService import BaseService

class TeamService(BaseService[Team, TeamCreate, TeamUpdate]):
    def __init__(self):
        super().__init__(TeamRepository())