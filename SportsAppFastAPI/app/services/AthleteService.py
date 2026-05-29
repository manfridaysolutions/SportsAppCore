from typing import List
from sqlmodel import select
from sqlalchemy.orm import selectinload, aliased
from sqlmodel.ext.asyncio.session import AsyncSession

from SportsAppModels.models.Athlete import (
    Athlete,
    AthleteCreate,
    AthleteUpdate,
)
from app.repositories.AthleteRepository import AthleteRepository
from app.services.BaseService import BaseService

from SportsAppModels.models.AthleteSport import ( AthleteSport )
from SportsAppModels.models.Contract import ( Contract )
from SportsAppModels.models.Season import ( Season )

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
    
    async def get_by_roster(
    self, 
    session: AsyncSession, 
    season_id: int, 
    team_id: int
    ) -> List[Athlete]:
        if not season_id or not team_id:
            return []

        # 1. Get the date range of the specific season the user is asking for
        target_season = await session.get(Season, season_id)
        if not target_season:
            return []

        # Aliases for the start and end seasons of the contract
        start_season_attr = aliased(Season)
        end_season_attr = aliased(Season)

        stmt = (
            select(Athlete)
            .join(Contract, Athlete.athlete_id == Contract.athlete_id)
            .join(start_season_attr, Contract.start_season_id == start_season_attr.season_id)
            .join(end_season_attr, Contract.end_season_id == end_season_attr.season_id)
            .where(Contract.team_id == team_id)
            .where(Contract.is_active == True)
            # 2. Chronological Check: 
            # The target season's dates must be within the contract's season dates
            .where(start_season_attr.start_date <= target_season.start_date)
            .where(end_season_attr.end_date >= target_season.end_date)
            .options(
                selectinload(Athlete.athlete_sports),
                selectinload(Athlete.rosters),
                selectinload(Athlete.nationality)
            )
            .distinct()
        )
                
        result = await session.exec(stmt)
        return result.all()