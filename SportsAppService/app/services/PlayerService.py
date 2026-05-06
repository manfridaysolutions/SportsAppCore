from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from SportsAppModels.models.Player import PlayerTradeRequest, PlayerUpdateRequest, PlayerCreateRequest, PlayerReadResponse

from app.repositories.AthleteRepository import AthleteRepository
from app.repositories.RosterRepository import RosterRepository
from app.repositories.RosterPositionRepository import RosterPositionRepository
from app.repositories.SeasonRepository import SeasonRepository

class PlayerService:

    def __init__(self):
        self.athletes = AthleteRepository()
        self.rosters = RosterRepository()
        self.roster_positions = RosterPositionRepository()
        self.seasons = SeasonRepository()

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
            for pos in payload.roster_positions:
                pos_data = pos.dict()
                pos_data["roster_id"] = roster.roster_id

                created = await self.roster_positions.create(session, pos_data)
                created_positions.append(created)

        return PlayerReadResponse(
            athlete=athlete,
            roster=roster,
            roster_positions=created_positions
        )
    
    async def get_players_by_season(
        self,
        session: AsyncSession,
        season_id: int, 
        team_id: Optional[int] = None
    ) -> list[PlayerReadResponse]:
        
        season = await self.seasons.get_by_id(session, season_id);

        league_id = season.league_id;

        rosters = await self.rosters.get_all(session, season_id = season_id)

        responses = []

        return responses
    
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
            roster_positions = []
            if roster:
                roster_positions = await self.roster_positions.get_positions_for_roster(
                    session,
                    roster.roster_id
                )

            responses.append(
                PlayerReadResponse(
                    athlete=athlete,
                    roster=roster,
                    roster_positions=roster_positions
                )
            )

        return responses

    async def update_player(
        self,
        session: AsyncSession,
        athlete_id: int,
        payload: PlayerUpdateRequest
    ) -> PlayerReadResponse:

        async with session.begin():

            # 1. Load existing athlete
            athlete = await self.athletes.get(session, athlete_id)
            if not athlete:
                raise ValueError(f"Athlete {athlete_id} not found")

            # 2. Load existing roster
            roster = await self.rosters.get_by_athlete(session, athlete_id)
            if not roster:
                raise ValueError(f"Roster for athlete {athlete_id} not found")

            # 3. Update athlete (patch)
            if payload.athlete:
                athlete = await self.athletes.update(
                    session,
                    athlete,
                    payload.athlete
                )

            # 4. Update roster (patch)
            if payload.roster:
                roster = await self.rosters.update(
                    session,
                    roster,
                    payload.roster
                )

            # 5. Replace roster positions (if provided)
            roster_positions = await self.roster_positions.get_positions_for_roster(
                session,
                roster.roster_id
            )

            if payload.positions is not None:
                # Delete existing positions
                for pos in roster_positions:
                    await self.roster_positions.delete(
                        session,
                        pos.roster_id,
                        pos.position_id
                    )

                # Insert new positions
                new_positions = []
                for pos in payload.positions:
                    pos_data = pos.dict()
                    pos_data["roster_id"] = roster.roster_id
                    created = await self.roster_positions.create(session, pos_data)
                    new_positions.append(created)

                roster_positions = new_positions

        return PlayerReadResponse(
            athlete=athlete,
            roster=roster,
            roster_positions=roster_positions
        )
    
    async def trade_player(
        self,
        session: AsyncSession,
        athlete_id: int,
        payload: PlayerTradeRequest
    ) -> PlayerReadResponse:

        async with session.begin():

            # 1. Load athlete
            athlete = await self.athletes.get(session, athlete_id)
            if not athlete:
                raise ValueError(f"Athlete {athlete_id} not found")

            # 2. Load current roster
            old_roster = await self.rosters.get_by_athlete(session, athlete_id)
            if not old_roster:
                raise ValueError(f"No roster found for athlete {athlete_id}")

            # 3. Mark old roster as inactive
            old_roster.status = "Traded"
            await self.rosters.update(session, old_roster, old_roster)

            # 4. Create new roster
            new_roster_data = payload.new_roster.dict()
            new_roster_data["athlete_id"] = athlete_id

            new_roster = await self.rosters.create(session, new_roster_data)

            # 5. Create new roster positions
            new_roster_positions = []
            for pos in payload.new_positions:
                pos_data = pos.dict()
                pos_data["roster_id"] = new_roster.roster_id

                created = await self.roster_positions.create(session, pos_data)
                new_roster_positions.append(created)

        return PlayerReadResponse(
            athlete=athlete,
            roster=new_roster,
            roster_positions=new_roster_positions
        )

    