from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories.RosterPositionRepository import RosterPositionRepository
from SportsAppModels.models.RosterPosition import (
    RosterPosition,
    RosterPositionCreate,
    RosterPositionUpdate
)

from app.services.BaseService import BaseService

class RosterPositionService(BaseService[
    RosterPosition,
    RosterPositionCreate,
    RosterPositionUpdate
]):

    def __init__(self):
        super().__init__(RosterPositionRepository())
        self.repo = RosterPositionRepository()

    async def get_positions_for_roster(
        self,
        session: AsyncSession,
        roster_id: int
    ) -> List[RosterPosition]:
        return await self.repo.get_positions_for_roster(session, roster_id)

    async def assign_position(
        self,
        session: AsyncSession,
        payload: RosterPositionCreate
    ) -> RosterPosition:
        # Prevent duplicate assignments
        existing = await self.repo.get(
            session,
            payload.roster_id,
            payload.position_id
        )
        if existing:
            return existing  # or raise an error depending on your rules

        return await self.repo.create(session, payload)

    async def update_position(
        self,
        session: AsyncSession,
        roster_id: int,
        position_id: int,
        payload: RosterPositionUpdate
    ) -> Optional[RosterPosition]:
        db_obj = await self.repo.get(session, roster_id, position_id)
        if not db_obj:
            return None

        return await self.repo.update(session, db_obj, payload)

    async def remove_position(
        self,
        session: AsyncSession,
        roster_id: int,
        position_id: int
    ) -> bool:
        return await self.repo.delete(session, roster_id, position_id)
