from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.services.PlayerOrchestrationService import PlayerOrchestrationService
from SportsAppModels.models.PlayerCreateRequest import PlayerCreateRequest
from SportsAppModels.models.PlayerReadResponse import PlayerReadResponse
from SportsAppModels.models.PlayerUpdateRequest import PlayerUpdateRequest
from SportsAppModels.models.PlayerTradeRequest import PlayerTradeRequest

player_endpoint = APIRouter(prefix="/players", tags=["Players"])

service = PlayerOrchestrationService()

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

@player_endpoint.post("/{athlete_id}/trade", response_model=PlayerReadResponse)
async def trade_player(
    athlete_id: int,
    payload: PlayerTradeRequest,
    session: AsyncSession = Depends(get_session)
):
    return await service.trade_player(session, athlete_id, payload)
