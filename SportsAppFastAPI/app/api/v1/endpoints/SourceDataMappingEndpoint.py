from typing import List
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import get_session
from app.services.SourceDataMappingService import SourceDataMappingService
from SportsAppModels.models.SourceDataMapping import SourceDataMappingCreate

# You will create this service next
mapping_service = SourceDataMappingService()
mapping_endpoint = APIRouter(prefix="/synch/mappings", tags=["Data Mapping"])

@mapping_endpoint.post("/check", response_model=List[SourceDataMappingCreate])
async def check_source_data_mappings(
    mappings: List[SourceDataMappingCreate], 
    session: AsyncSession = Depends(get_session)
):
    """
    Generic check to see which external mappings exist in the system.
    Returns only the items from the input list that are NOT currently in the database.
    """
    return await mapping_service.get_missing_mappings(session, mappings)