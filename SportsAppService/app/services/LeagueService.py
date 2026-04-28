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
    
    async def get_all(self, session: AsyncSession, **kwargs) -> List[League]:
        sport_id = kwargs.get("sport_id")
        
        # Start the statement and include the country relationship immediately
        statement = select(League).options(selectinload(League.country))
        
        if sport_id:
            statement = statement.where(League.sport_id == int(sport_id))
            
        results = await session.exec(statement)
        return results.all()