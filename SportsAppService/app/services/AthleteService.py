from typing import List
from sqlmodel import select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from SportsAppModels.models.Athlete import (
    Athlete,
    AthleteCreate,
    AthleteUpdate,
)
from app.repositories.AthleteRepository import AthleteRepository
from app.services.BaseService import BaseService

from SportsAppModels.models.AthleteSport import ( AthleteSport )

class AthleteService(BaseService[Athlete, AthleteCreate, AthleteUpdate]):
    def __init__(self):
        super().__init__(AthleteRepository())

    async def get_by_sport(self, session: AsyncSession, sport_id: int) -> List[Athlete]:
        if not sport_id:
            return []
        
        stmt = (
            select(Athlete)
            .join(Athlete.athlete_sports)
            .join(Athlete.rosters, isouter=True)
            .where(AthleteSport.sport_id == sport_id)
            .options(
                selectinload(Athlete.athlete_sports),
                selectinload(Athlete.rosters),
                selectinload(Athlete.nationality)
            )
            .distinct()
        )
                
        result = await session.exec(stmt)

        return result.all()