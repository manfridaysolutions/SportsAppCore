from typing import List

from SportsAppModels.models.Athlete import (
    Athlete,
    AthleteCreate,
    AthleteUpdate,
    AthleteRead
)
from app.services.AthleteService import AthleteService
from app.api.v1.endpoints.BaseEndpoint import BaseEndpoint
from app.db.session import get_session

from fastapi import Query, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

athlete_service = AthleteService()

athlete_endpoint = BaseEndpoint[
    Athlete,
    AthleteCreate,
    AthleteUpdate,
    AthleteRead
](
    service=athlete_service,
    model_create=AthleteCreate,
    model_read=AthleteRead,
    model_update=AthleteUpdate,
    prefix="/athlete",
    tags=["Athlete"]
).router

@athlete_endpoint.get(
    "/by-sport/",
    response_model=List[AthleteRead], summary="Get Athletes by sport"
)

async def get_athlete_by_sport(
    sport_id: int = Query(..., description="sport_id to filter by"),
    session: AsyncSession = Depends(get_session)
):
    return await athlete_service.get_by_sport(session, sport_id)