from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from SportsAppModels.models.Roster import (
    Roster,
    RosterCreate,
    RosterUpdate,
)

from app.repositories.BaseRepository import BaseRepository

class RosterRepository(BaseRepository[
    Roster,
    RosterCreate, 
    RosterUpdate
]):
    def __init__(self):
        super().__init__(Roster)

    async def get_by_athlete(
        self,
        session: AsyncSession,
        athlete_id: int
    ) -> Optional[Roster]:
        stmt = (
            select(Roster)
            .where(Roster.athlete_id == athlete_id)
        )

        result = await session.exec(stmt)
        return result.first()