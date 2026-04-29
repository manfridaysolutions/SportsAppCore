from typing import List

from sqlmodel.ext.asyncio.session import AsyncSession

from SportsAppModels.models.Position import (
    Position,
    PositionCreate,
    PositionUpdate,
)
from app.repositories.PositionRepository import PositionRepository
from app.services.BaseService import BaseService

from sqlmodel import select
from sqlalchemy.orm import selectinload

class PositionService(BaseService[Position, PositionCreate, PositionUpdate]):
    def __init__(self):
        super().__init__(PositionRepository())
    
    async def get_all(self, session: AsyncSession, **kwargs) -> List[Position]:
        sport_id = kwargs.get("sport_id")
        
        # Start the statement and include the country relationship immediately
        statement = select(Position).options(selectinload(Position.roster_positions))
        
        if sport_id:
            statement = statement.where(Position.sport_id == int(sport_id))
            
        results = await session.exec(statement)
        return results.all()