from typing import Generic, TypeVar, Optional, List

from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories.BaseRepository import BaseRepository
from sqlmodel import SQLModel


ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, repository: BaseRepository[ModelType, CreateSchemaType, UpdateSchemaType]):
        self.repository = repository

    async def get_all(self, session: AsyncSession, **kwargs) -> List[ModelType]:
        return await self.repository.get_all(session)

    async def get_by_id(self, session: AsyncSession, id: int) -> Optional[ModelType]:
        return await self.repository.get_by_id(session, id)

    async def create(self, session: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        return await self.repository.create(session, obj_in)

    async def update(
        self,
        session: AsyncSession,
        id: int,
        obj_in: UpdateSchemaType
    ) -> Optional[ModelType]:

        db_obj = await self.repository.get_by_id(session, id)
        if not db_obj:
            return None

        return await self.repository.update(session, db_obj, obj_in)

    async def delete(self, session: AsyncSession, id: int) -> bool:
        db_obj = await self.repository.get_by_id(session, id)
        if not db_obj:
            return False

        await self.repository.delete(session, db_obj)
        return True
