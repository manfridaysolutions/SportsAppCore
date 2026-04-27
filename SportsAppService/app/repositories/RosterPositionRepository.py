from typing import Optional, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.orm import selectinload

from SportsAppModels.models.RosterPosition import (
    RosterPosition,
    RosterPositionCreate,
    RosterPositionUpdate
)

class RosterPositionRepository :

    async def get_positions_for_roster(
        self,
        session: AsyncSession,
        roster_id: int
    ) -> List[RosterPosition]:
        stmt = (
            select(RosterPosition)
            .where(RosterPosition.roster_id == roster_id)
            .options(
                selectinload(RosterPosition.position),
                selectinload(RosterPosition.roster)
            )
        )
        result = await session.exec(stmt)
        return result.all()

    async def get(
        self,
        session: AsyncSession,
        roster_id: int,
        position_id: int
    ) -> Optional[RosterPosition]:
        stmt = (
            select(RosterPosition)
            .where(
                RosterPosition.roster_id == roster_id,
                RosterPosition.position_id == position_id
            )
            .options(
                selectinload(RosterPosition.position),
                selectinload(RosterPosition.roster)
            )
        )
        result = await session.exec(stmt)
        return result.one_or_none()

    async def create(
        self,
        session: AsyncSession,
        payload: RosterPositionCreate
    ) -> RosterPosition:
        obj = RosterPosition(**payload.dict())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def update(
        self,
        session: AsyncSession,
        db_obj: RosterPosition,
        payload: RosterPositionUpdate
    ) -> RosterPosition:
        update_data = payload.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_obj, key, value)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(
        self,
        session: AsyncSession,
        roster_id: int,
        position_id: int
    ) -> bool:
        obj = await self.get(session, roster_id, position_id)
        if not obj:
            return False

        await session.delete(obj)
        await session.commit()
        return True
