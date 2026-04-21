from typing import Generic, TypeVar, Type, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.services.BaseService import BaseService
from sqlmodel import SQLModel


ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=SQLModel)


class BaseEndpoint(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ReadSchemaType]):

    def __init__(
        self,
        *,
        service: BaseService[ModelType, CreateSchemaType, UpdateSchemaType],
        model_read: Type[ReadSchemaType],
        prefix: str,
        tags: list[str]
    ):
        self.router = APIRouter(prefix=prefix, tags=tags)
        self.service = service
        self.model_read = model_read

        self._add_routes()

    def _add_routes(self):

        @self.router.get("/", response_model=List[self.model_read])
        async def get_all(session: AsyncSession = Depends(get_session)):
            return await self.service.get_all(session)

        @self.router.get("/{id}", response_model=self.model_read)
        async def get_by_id(id: int, session: AsyncSession = Depends(get_session)):
            obj = await self.service.get_by_id(session, id)
            if not obj:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            return obj

        @self.router.post("/", response_model=self.model_read, status_code=status.HTTP_201_CREATED)
        async def create(
            obj_in: CreateSchemaType,
            session: AsyncSession = Depends(get_session)
        ):
            return await self.service.create(session, obj_in)

        @self.router.put("/{id}", response_model=self.model_read)
        async def update(
            id: int,
            obj_in: UpdateSchemaType,
            session: AsyncSession = Depends(get_session)
        ):
            updated = await self.service.update(session, id, obj_in)
            if not updated:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            return updated

        @self.router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete(id: int, session: AsyncSession = Depends(get_session)):
            deleted = await self.service.delete(session, id)
            if not deleted:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            return None
