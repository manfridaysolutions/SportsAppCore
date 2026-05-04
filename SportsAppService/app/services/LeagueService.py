from typing import List

from sqlmodel.ext.asyncio.session import AsyncSession

from SportsAppModels.models.League import (
    League,
    LeagueCreate,
    LeagueUpdate,
)
from app.repositories.LeagueRepository import LeagueRepository
from app.services.BaseService import BaseService

from sqlmodel import select
from sqlalchemy.orm import selectinload

class LeagueService(BaseService[League, LeagueCreate, LeagueUpdate]):
    def __init__(self):
        super().__init__(LeagueRepository())