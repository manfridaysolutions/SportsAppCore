from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession

from SportsAppModels.models.PlayerCreateRequest import PlayerCreateRequest
from SportsAppModels.models.PlayerReadResponse import PlayerReadResponse

from app.repositories.AthleteRepository import AthleteRepository
from app.repositories.RosterRepository import RosterRepository
from app.repositories.RosterPositionRepository import RosterPositionRepository


class PlayerOrchestrationService:

    def __init__(self):
        self.athletes = AthleteRepository()
        self.rosters = RosterRepository()
        self.roster_positions = RosterPositionRepository()

    async def create_player(
        self,
        session: AsyncSession,
        payload: PlayerCreateRequest
    ) -> PlayerReadResponse:

        async with session.begin():  # Transaction boundary

            # 1. Create Athlete
            athlete = await self.athletes.create(session, payload.athlete)

            # 2. Create Roster (inject athlete_id)
            roster_data = payload.roster.dict()
            roster_data["athlete_id"] = athlete.athlete_id
            roster = await self.rosters.create(session, roster_data)

            # 3. Create Roster Positions
            created_positions = []
            for pos in payload.positions:
                pos_data = pos.dict()
                pos_data["roster_id"] = roster.roster_id

                created = await self.roster_positions.create(session, pos_data)
                created_positions.append(created)

        return PlayerReadResponse(
            athlete=athlete,
            roster=roster,
            positions=created_positions
        )
    
    async def get_all_players(
        self,
        session: AsyncSession
    ) -> list[PlayerReadResponse]:

        # 1. Get all athletes
        athletes = await self.athletes.get_all(session)

        responses = []

        for athlete in athletes:

            # 2. Get roster for athlete
            roster = await self.rosters.get_by_athlete(session, athlete.athlete_id)

            # 3. Get positions for roster
            positions = []
            if roster:
                positions = await self.roster_positions.get_positions_for_roster(
                    session,
                    roster.roster_id
                )

            responses.append(
                PlayerReadResponse(
                    athlete=athlete,
                    roster=roster,
                    positions=positions
                )
            )

        return responses

    
    
