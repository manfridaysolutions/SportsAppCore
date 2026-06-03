from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import get_session
from app.services.AthleteSynchService import AthleteSynchService
from SportsAppModels.models.Athlete import AthleteRead, AthleteSynch

athlete_synch_service = AthleteSynchService()
athlete_synch_endpoint = APIRouter(prefix="/synch/athletes", tags=["Athlete Synchronization"])

@athlete_synch_endpoint.post("/upsert", response_model=List[AthleteRead], status_code=status.HTTP_201_CREATED)
async def upsert_athletes(payload: List[AthleteSynch], session: AsyncSession = Depends(get_session)):
    """
    Processes a bulk array of athlete payloads. Creates new Athlete records 
    and establishes the SourceDataMapping entries.
    """
    return await athlete_synch_service.upsert_synced_athletes(session, payload)