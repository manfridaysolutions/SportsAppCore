from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from SportsAppModels.models.Position import (
    Position    
)

from app.repositories.BaseRepository import BaseRepository

class PositionRepository(BaseRepository[
    Position
]):
    def __init__(self):
        super().__init__(Position)