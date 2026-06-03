from typing import List
from sqlmodel import select, and_, Session
from SportsAppModels.models.SourceDataMapping import SourceDataMapping, SourceDataMappingCreate

class SourceDataMappingService:
    async def get_missing_mappings(self, session: Session, mappings: List[SourceDataMappingCreate]) -> List[SourceDataMappingCreate]:
        # 1. Group by entity_type to make the query more efficient if checking multiple types
        # For now, we assume all mappings in the list share the same entity_type
        if not mappings:
            return []

        entity_type = mappings[0].entity_type
        external_ids = [m.external_id for m in mappings]
        
        # 2. Query existing mappings
        stmt = select(SourceDataMapping).where(
            and_(
                SourceDataMapping.entity_type == entity_type,
                SourceDataMapping.external_id.in_(external_ids)
            )
        )
        results = await session.exec(stmt)
        existing_mappings = {m.external_id for m in results.all()}

        # 3. Filter out what we already have
        return [m for m in mappings if m.external_id not in existing_mappings]