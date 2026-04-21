from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.services.RosterPositionService import RosterPositionService
from SportsAppModels.models.RosterPosition import (
    RosterPositionRead,
    RosterPositionCreate,
    RosterPositionUpdate
)


router = APIRouter(prefix="/rosters", tags=["Roster Positions"])

service = RosterPositionService()


@router.get("/{roster_id}/positions", response_model=list[RosterPositionRead])
async def get_positions_for_roster(
    roster_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await service.get_positions_for_roster(session, roster_id)


@router.post("/{roster_id}/positions", response_model=RosterPositionRead, status_code=status.HTTP_201_CREATED)
async def assign_position_to_roster(
    roster_id: int,
    payload: RosterPositionCreate,
    session: AsyncSession = Depends(get_session)
):
    if payload.roster_id != roster_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="roster_id in URL and body must match"
        )

    return await service.assign_position(session, payload)


@router.put("/{roster_id}/positions/{position_id}", response_model=RosterPositionRead)
async def update_roster_position(
    roster_id: int,
    position_id: int,
    payload: RosterPositionUpdate,
    session: AsyncSession = Depends(get_session)
):
    updated = await service.update_position(session, roster_id, position_id, payload)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return updated


@router.delete("/{roster_id}/positions/{position_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_position_from_roster(
    roster_id: int,
    position_id: int,
    session: AsyncSession = Depends(get_session)
):
    deleted = await service.remove_position(session, roster_id, position_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return None
