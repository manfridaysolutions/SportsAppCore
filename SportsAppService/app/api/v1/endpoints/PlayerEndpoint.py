from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.services.PlayerService import PlayerService
from SportsAppModels.models.Player import PlayerCreateRequest, PlayerReadResponse, PlayerUpdateRequest, PlayerTradeRequest

player_endpoint = APIRouter(prefix="/players", tags=["Players"])

service = PlayerService()

@player_endpoint.post("/", response_model=PlayerReadResponse, status_code=status.HTTP_201_CREATED)
async def create_player(
    payload: PlayerCreateRequest,
    session: AsyncSession = Depends(get_session)
):
    return await service.create_player(session, payload)

@player_endpoint.put("/{athlete_id}", response_model=PlayerReadResponse)
async def update_player(
    athlete_id: int,
    payload: PlayerUpdateRequest,
    session: AsyncSession = Depends(get_session)
):
    return await service.update_player(session, athlete_id, payload)

@player_endpoint.get("/", response_model=list[PlayerReadResponse])
async def get_all_players(
    session: AsyncSession = Depends(get_session)
):
    return await service.get_all_players(session)

@player_endpoint.get("/{season_id}", response_model=list[PlayerReadResponse])
async def get_players_by_season(
    season_id: int,
    team_id: Optional[int] = None,
    session: AsyncSession = Depends(get_session)
):
    return await service.get_players_by_season(session, season_id, team_id)

@player_endpoint.post("/{athlete_id}/trade", response_model=PlayerReadResponse)
async def trade_player(
    athlete_id: int,
    payload: PlayerTradeRequest,
    session: AsyncSession = Depends(get_session)
):
    return await service.trade_player(session, athlete_id, payload)
