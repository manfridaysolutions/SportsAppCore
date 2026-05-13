from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from SportsAppModels.models.RosterPosition import (
    RosterPosition,
    RosterPositionCreate,
    RosterPositionUpdate
)

from app.repositories.BaseRepository import BaseRepository

class RosterPositionRepository(BaseRepository[
    RosterPosition,
    RosterPositionCreate,
    RosterPositionUpdate
]):
    default_relationships = ["roster","position"]  # Automatically load related categories
    
    def __init__(self):
        super().__init__(RosterPosition)