from typing import List
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from SportsAppModels.models.ReferenceCategory import (
    ReferenceCategory,
    ReferenceCategoryCreate,
    ReferenceCategoryUpdate
)
from app.repositories.ReferenceCategoryRepository import ReferenceCategoryRepository
from app.services.BaseService import BaseService

class ReferenceCategoryService(BaseService[
    ReferenceCategory,
    ReferenceCategoryCreate,
    ReferenceCategoryUpdate
]):
    def __init__(self):
        super().__init__(ReferenceCategoryRepository())
        self.reference_categories = ReferenceCategoryRepository()

    async def get_by_names(self, session: AsyncSession, names: List[str]) -> List[ReferenceCategory]:

        if not names:
            return []
        
        stmt = (
            select(ReferenceCategory)
            .where(ReferenceCategory.name.in_(names))
            .options(selectinload(ReferenceCategory.reference_values))
        )
        
        result = await session.exec(stmt)

        return result.all()
