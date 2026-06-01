from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.services.TeamSynchService import TeamSynchService
from SportsAppModels.models.Team import TeamRead
from SportsAppModels.models.TeamSynch import TeamSynch

team_synch_service = TeamSynchService()

team_synch_endpoint = APIRouter(prefix="/synch/teams", tags=["Team Synchronization"])

@team_synch_endpoint.post("/", response_model=List[TeamRead], status_code=status.HTTP_201_CREATED)
async def synchronize_teams(
    payload: List[TeamSynch], 
    session: AsyncSession = Depends(get_session)
):
    """
    Endpoint dedicated to external background sync workers.
    Processes a bulk array of compound team payloads and executes lookups against 
    source data mapping tables to automatically coordinate creation or updates.
    """
    return await team_synch_service.upsert_synced_teams(session, payload)