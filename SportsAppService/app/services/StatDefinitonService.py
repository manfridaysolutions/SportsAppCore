from typing import List

from sqlmodel.ext.asyncio.session import AsyncSession

from SportsAppModels.models.StatDefinition import (
    StatDefinition,
    StatDefinitionCreate,
    StatDefinitionUpdate,
)
from app.repositories.StatDefinitionRepository import StatDefinitionRepository
from app.services.BaseService import BaseService

from sqlmodel import select
from sqlalchemy.orm import selectinload

class StatDefinitionService(BaseService[StatDefinition, StatDefinitionCreate, StatDefinitionUpdate]):
    def __init__(self):
        super().__init__(StatDefinitionRepository())