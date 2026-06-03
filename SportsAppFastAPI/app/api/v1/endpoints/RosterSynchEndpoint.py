from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.services.RosterSynchService import RosterSynchService
from SportsAppModels.models.Roster import RosterRead
from SportsAppModels.models.RosterSynch import RosterSynch

roster_synch_service = RosterSynchService()

roster_synch_endpoint = APIRouter(prefix="/synch/rosters", tags=["Roster Synchronization"])

@roster_synch_endpoint.post("/", response_model=List[RosterRead], status_code=status.HTTP_201_CREATED)
async def synchronize_rosters(
    payload: List[RosterSynch], 
    session: AsyncSession = Depends(get_session)
):
    """
    Endpoint dedicated to external background sync workers.
    Processes a bulk array of compound roster payloads and executes lookups against 
    source data mapping tables to automatically coordinate creation or updates.
    """
    return await roster_synch_service.upsert_synced_rosters(session, payload)