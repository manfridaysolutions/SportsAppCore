from typing import List
from sqlmodel import select, Session
from SportsAppModels.models.SourceDataMapping import SourceDataMapping
from SportsAppModels.models.Athlete import Athlete, AthleteBase
from SportsAppModels.models.AthleteSynch import AthleteSynch

class AthleteSynchService:
    async def upsert_synced_athletes(self, session: Session, payload: List[AthleteSynch]) -> List[Athlete]:
        upserted_athletes = []
        
        for athlete_data in payload:
            # 1. Ensure the mapping data exists in the payload before proceeding
            if not athlete_data.source_data_mapping:
                continue
                
            external_id_str = str(athlete_data.source_data_mapping.external_id)
            source_system_str = athlete_data.source_data_mapping.source_system
            
            # 2. Check if mapping already exists for this external_id
            stmt = select(SourceDataMapping).where(
                SourceDataMapping.entity_type == "Athlete",
                SourceDataMapping.source_system == source_system_str,
                SourceDataMapping.external_id == external_id_str
            )
            result = await session.exec(stmt)
            mapping = result.one_or_none()
            
            if mapping:
                # Athlete already exists, fetch and add to return list
                athlete = await session.get(Athlete, mapping.internal_id)
                upserted_athletes.append(athlete)
            else:
                # 3. Create the new Athlete record
                new_athlete = Athlete(
                    display_name=athlete_data.display_name,
                    first_name=athlete_data.first_name,
                    last_name=athlete_data.last_name,
                    birth_date=athlete_data.birth_date
                )
                session.add(new_athlete)
                await session.flush()  # Get the generated internal_id
                
                # 4. Create the mapping
                new_mapping = SourceDataMapping(
                    entity_type="Athlete",
                    source_system=source_system_str,
                    external_id=external_id_str,
                    internal_id=new_athlete.id
                )
                session.add(new_mapping)
                upserted_athletes.append(new_athlete)
        
        await session.commit()
        return upserted_athletes