from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from SportsAppModels.models.Position import (
    Position,
    PositionCreate,
    PositionUpdate
)

from app.repositories.BaseRepository import BaseRepository

class PositionRepository(BaseRepository[
    Position,
    PositionCreate,
    PositionUpdate
]):
    default_relationships = ["roster_positions"]  # Automatically load related categories

    def __init__(self):
        super().__init__(Position)