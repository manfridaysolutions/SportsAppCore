from typing import List
from sqlmodel import select, Session
from SportsAppModels.models.SourceDataMapping import SourceDataMapping
from SportsAppModels.models.Athlete import Athlete, AthleteSynch

class AthleteSynchService:
    async def upsert_synced_athletes(self, session: Session, payload: List[AthleteSynch]) -> List[Athlete]:
        upserted_athletes = []
        
        for athlete_data in payload:
            # 1. Check if mapping already exists for this external_id
            stmt = select(SourceDataMapping).where(
                SourceDataMapping.entity_type == "Athlete",
                SourceDataMapping.source_system == "MLB_API",
                SourceDataMapping.external_id == str(athlete_data.external_id)
            )
            result = await session.exec(stmt)
            mapping = result.one_or_none()
            
            if mapping:
                # Athlete already exists, fetch and add to return list
                athlete = await session.get(Athlete, mapping.internal_id)
                upserted_athletes.append(athlete)
            else:
                # 2. Create the new Athlete record
                new_athlete = Athlete(
                    display_name=athlete_data.display_name,
                    first_name=athlete_data.first_name,
                    last_name=athlete_data.last_name
                )
                session.add(new_athlete)
                await session.flush()  # Get the generated internal_id
                
                # 3. Create the mapping
                new_mapping = SourceDataMapping(
                    entity_type="Athlete",
                    source_system="MLB_API",
                    external_id=str(athlete_data.external_id),
                    internal_id=new_athlete.id
                )
                session.add(new_mapping)
                upserted_athletes.append(new_athlete)
        
        await session.commit()
        return upserted_athletes