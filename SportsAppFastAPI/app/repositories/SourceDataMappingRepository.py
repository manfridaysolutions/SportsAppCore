from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from SportsAppModels.models.SourceDataMapping import (
    SourceDataMapping,
    SourceDataMappingCreate,
    SourceDataMappingUpdate
)

from app.repositories.BaseRepository import BaseRepository

class SourceDataMappingRepository(BaseRepository[
    SourceDataMapping, 
    SourceDataMappingCreate,
    SourceDataMappingUpdate
]):
    def __init__(self):
        super().__init__(SourceDataMapping)

    async def get_by_external_id(
        self, 
        session: AsyncSession, 
        source_system: str, 
        external_id: str, 
        entity_type: str
    ) -> Optional[SourceDataMapping]:
        """
        Utility lookup to quickly find an existing internal mapping record 
        using identity markers provided by external sports APIs.
        """
        statement = select(self.model).where(
            self.model.source_system == source_system,
            self.model.external_id == external_id,
            self.model.entity_type == entity_type
        )
        result = await session.exec(statement)
        return result.first()
    
    async def get_bulk_mappings(
        self, 
        session: AsyncSession, 
        source_system: str, 
        external_ids: List[str], 
        entity_type: str
    ) -> List[SourceDataMapping]:
        """
        Fetches and returns raw mapping records in bulk for a list of external IDs.
        """
        if not external_ids:
            return []

        statement = select(self.model).where(
            self.model.source_system == source_system,
            self.model.entity_type == entity_type,
            self.model.external_id.in_(external_ids)
        )
        
        result = await session.exec(statement)
        # .all() returns a Sequence, casting to a List satisfies the type hint cleanly
        return list(result.all())