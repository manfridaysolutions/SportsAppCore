from typing import List
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from SportsAppModels.models.ReferenceValue import (
    ReferenceValue,
    ReferenceValueCreate,
    ReferenceValueUpdate
)
from app.repositories.ReferenceValueRepository import ReferenceValueRepository
from app.services.BaseService import BaseService

class ReferenceValueService(BaseService[
    ReferenceValue,
    ReferenceValueCreate,
    ReferenceValueUpdate
]):
    def __init__(self):
        super().__init__(ReferenceValueRepository())

    async def get_all(self, session: AsyncSession, **kwargs) -> List[ReferenceValue]    :
        reference_category_id = kwargs.get("reference_category_id")
        
        # Start the statement and include the country relationship immediately
        statement = select(ReferenceValue).options(selectinload(ReferenceValue.reference_category))
        
        if reference_category_id:
            statement = statement.where(ReferenceValue.reference_category_id == int(reference_category_id))
            
        results = await session.exec(statement)
        return results.all()