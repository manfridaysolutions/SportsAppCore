from typing import List
from fastapi import APIRouter, Query, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.services.AthleteService import AthleteService
from app.api.v1.endpoints.BaseEndpoint import BaseEndpoint
from SportsAppModels.models.Athlete import (
    Athlete,
    AthleteCreate,
    AthleteUpdate,
    AthleteRead
)

athlete_service = AthleteService()

# 1. Create the router that main.py will use
# IMPORTANT: This router holds the priority
athlete_endpoint = APIRouter(prefix="/athlete", tags=["Athlete"])

# 2. Define your specific filters FIRST on this router
@athlete_endpoint.get("/by-sport", response_model=List[AthleteRead])
async def get_athlete_by_sport(
    sport_id: int = Query(...),
    session: AsyncSession = Depends(get_session)
):
    return await athlete_service.get_by_sport(session, sport_id)

@athlete_endpoint.get("/by-roster", response_model=List[AthleteRead])
async def get_athlete_by_roster(
    season_id: int = Query(...),
    team_id: int = Query(...),
    session: AsyncSession = Depends(get_session)
):
    return await athlete_service.get_by_roster(
        session, 
        season_id=season_id, 
        team_id=team_id
    )

# 3. Generate the Base CRUD routes
# Use prefix="" so it doesn't nest like /athlete/athlete/
base_endpoint = BaseEndpoint[
    Athlete,
    AthleteCreate,
    AthleteUpdate,
    AthleteRead
](
    service=athlete_service,
    model_create=AthleteCreate,
    model_read=AthleteRead,
    model_update=AthleteUpdate,
    prefix="", 
    tags=["Athlete"]
)

# 4. Include the base routes LAST
athlete_endpoint.include_router(base_endpoint.router)