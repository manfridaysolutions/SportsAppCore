from typing import List
from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from SportsAppModels.models.Team import Team
from SportsAppModels.models.TeamSynch import TeamSynch
from SportsAppModels.models.SourceDataMapping import SourceDataMapping

from app.repositories.TeamRepository import TeamRepository
from app.repositories.SourceDataMappingRepository import SourceDataMappingRepository

class TeamSynchService:
    def __init__(self):
        self.team_repo = TeamRepository()
        self.mapping_repo = SourceDataMappingRepository()

    async def upsert_synced_teams(self, session: AsyncSession, payload: List[TeamSynch]) -> List[Team]:
        """
        Coordinates batch team synchronization using native SQLModel session execution.
        Resolves identities using source mappings with a fallback business key fallback logic.
        """
        synced_teams = []

        for team_data in payload:
            mapping_info = team_data.source_data_mapping
            db_team = None

            # 1. Primary Identity Path: Try resolving via SourceDataMapping table
            if mapping_info:
                statement = select(SourceDataMapping).where(
                    SourceDataMapping.source_system == mapping_info.source_system,
                    SourceDataMapping.external_id == mapping_info.external_id,
                    SourceDataMapping.entity_type == "Team"
                )
                # Native SQLModel execution returns scalar result wrappers directly 🚀
                result = await session.exec(statement)
                mapping_record = result.one_or_none()

                if mapping_record:
                    db_team = await session.get(Team, mapping_record.internal_id)

            # 2. Fallback Identity Path: Check Unique Business Constraint (League + Name)
            if not db_team and team_data.league_id and team_data.team_name:
                constraint_statement = select(Team).where(
                    Team.league_id == team_data.league_id,
                    Team.team_name == team_data.team_name
                )
                constraint_result = await session.exec(constraint_statement)
                db_team = constraint_result.one_or_none()

                # Self-healing: Link the missing mapping link right now
                if db_team and mapping_info:
                    db_mapping = SourceDataMapping(
                        entity_type=mapping_info.entity_type,
                        source_system=mapping_info.source_system,
                        external_id=mapping_info.external_id,
                        internal_id=db_team.team_id  
                    )
                    session.add(db_mapping)

            # 3. Route to proper Execution Path
            if db_team:
                # --- UPDATE PATH ---
                update_fields = team_data.model_dump(exclude_unset=True, exclude={"source_data_mapping"})
                for key, value in update_fields.items():
                    setattr(db_team, key, value)
                session.add(db_team)
            else:
                # --- INSERT PATH ---
                insert_fields = team_data.model_dump(exclude={"source_data_mapping"})
                db_team = Team.model_validate(insert_fields)
                
                session.add(db_team)
                await session.flush()  # Allocates db_team.team_id

                if mapping_info:
                    db_mapping = SourceDataMapping(
                        entity_type=mapping_info.entity_type,
                        source_system=mapping_info.source_system,
                        external_id=mapping_info.external_id,
                        internal_id=db_team.team_id  
                    )
                    session.add(db_mapping)

            synced_teams.append(db_team)

        # Commit everything atomically inside a single transaction unit
        await session.commit()

        for team in synced_teams:
            await session.refresh(team)

        return synced_teams