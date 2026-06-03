import httpx
from typing import List, Dict
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from SportsAppModels.models.Athlete import Athlete
from SportsAppModels.models.Roster import Roster
from SportsAppModels.models.RosterSynch import RosterSynch
from SportsAppModels.models.RosterPosition import RosterPosition
from SportsAppModels.models.SourceDataMapping import SourceDataMapping
from app.repositories.RosterRepository import RosterRepository

class RosterSynchService:
    def __init__(self):
        self.roster_repo = RosterRepository()
        self.position_api_url = "http://localhost:8000/api/v1/position/?sport_id=2"

    async def _get_position_map(self, session: AsyncSession) -> Dict[str, int]:
        """
        Fetches positions from the internal API and builds a mapping 
        dictionary: {'shortstop': 21, 'pitcher': 16, ...}
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(self.position_api_url)
            if response.status_code == 200:
                return {str(pos["position_name"]).lower(): pos["position_id"] 
                        for pos in response.json()}
        return {}

    async def upsert_synced_rosters(self, session: AsyncSession, payload: List[RosterSynch]) -> List[Roster]:
        synced_rosters = []
        pos_map = await self._get_position_map(session)

        for roster_data in payload:
            db_roster = None
            mapping_info = roster_data.source_data_mapping

            # 1. Resolve Athlete ID
            # Search for an existing mapping from the MLB Person ID to your internal ID
            mapping_stmt = select(SourceDataMapping).where(
                SourceDataMapping.source_system == "MLB_API",
                SourceDataMapping.external_id == str(roster_data.source_data_mapping.external_id), # MLB's ID
                SourceDataMapping.entity_type == "Athlete"
            )
            mapping_result = await session.exec(mapping_stmt)
            mapping_record = mapping_result.one_or_none()

            if mapping_record:
                internal_athlete_id = mapping_record.internal_id
            else:
                # Create a new Athlete record
                new_athlete = Athlete(
                    display_name=roster_data.athlete.display_name,
                    first_name=roster_data.athlete.first_name,
                    last_name=roster_data.athlete.last_name
                ) # Or fetch details

                session.add(new_athlete)
                await session.flush()
                internal_athlete_id = new_athlete.athlete_id
                
                # Create the mapping so we never have to do this again
                new_mapping = SourceDataMapping(
                    entity_type="Athlete",
                    source_system="MLB_API",
                    external_id=str(roster_data.athlete_id),
                    internal_id=internal_athlete_id
                )
                session.add(new_mapping)

            # # 2. Identity Resolution (SourceDataMapping)
            # # Using 'Roster' entity_type for the team+athlete+season unique combination
            # if mapping_info:
            #     statement = select(SourceDataMapping).where(
            #         SourceDataMapping.source_system == mapping_info.source_system,
            #         SourceDataMapping.external_id == mapping_info.external_id,
            #         SourceDataMapping.entity_type == "Roster" 
            #     )
            #     result = await session.exec(statement)
            #     mapping_record = result.one_or_none()
            #     if mapping_record:
            #         db_roster = await session.get(Roster, mapping_record.internal_id)

            # # 3. Identity Fallback (Team + Athlete + Season Business Key)
            # if not db_roster and all([roster_data.team_id, roster_data.athlete_id, roster_data.season_id]):
            #     constraint_statement = select(Roster).where(
            #         Roster.team_id == roster_data.team_id,
            #         Roster.athlete_id == internal_athlete_id,
            #         Roster.season_id == roster_data.season_id # Added season_id to constraint
            #     )
            #     result = await session.exec(constraint_statement)
            #     db_roster = result.one_or_none()

            # # 4. Execution Path (Insert or Update)
            # if db_roster:
            #     update_fields = roster_data.model_dump(exclude_unset=True, exclude={"source_data_mapping", "roster_positions"})
            #     for key, value in update_fields.items():
            #         setattr(db_roster, key, value)
            #     session.add(db_roster)
            # else:
            #     insert_fields = roster_data.model_dump(exclude={"source_data_mapping", "roster_positions"})
            #     db_roster = Roster.model_validate(insert_fields)
            #     session.add(db_roster)
            #     await session.flush()  

            # # 5. Map Roster Positions
            # # ... (your existing position mapping logic remains the same) ...
            
            # synced_rosters.append(db_roster)

        await session.commit()
        for roster in synced_rosters:
            await session.refresh(roster)

        return synced_rosters