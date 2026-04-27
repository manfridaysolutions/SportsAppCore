from typing import Generic, TypeVar, Type, Optional, List
from sqlmodel import SQLModel, select, inspect
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    # Default to an empty list so it doesn't break other models
    default_relationships: list = []

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_all(self, session: AsyncSession) -> List[ModelType]:
        statement = select(self.model)

        if self.default_relationships:
            for rel in self.default_relationships:
                # If it's already a class attribute (e.g., Sport.sport_category), use it
                # If it's a string, look it up on the class
                prop = rel if not isinstance(rel, str) else getattr(self.model, rel)
                
                # Ensure we are passing the attribute directly to selectinload
                statement = statement.options(selectinload(prop))

        result = await session.exec(statement)

        return result.all()

    async def get_by_id(
        self,
        session: AsyncSession,
        id: int
    ) -> Optional[ModelType]:
        # Resolve primary key column dynamically
        mapper = inspect(self.model)
        pk_cols = list(mapper.primary_key)

        if len(pk_cols) != 1:
            # For composite keys, this generic method is not suitable
            # and should be overridden in the concrete repository.
            raise ValueError(
                f"{self.model.__name__} has composite or no primary key; "
                "override get_by_id in the concrete repository."
            )

        pk_col = pk_cols[0]

        stmt = select(self.model).where(pk_col == id)

        if self.default_relationships:
            for rel in self.default_relationships:
                prop = rel if not isinstance(rel, str) else getattr(self.model, rel)
                stmt = stmt.options(selectinload(prop))

        result = await session.exec(stmt)
        return result.one_or_none()

    async def create(self, session: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        obj = self.model.from_orm(obj_in)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def update(
        self,
        session: AsyncSession,
        db_obj: ModelType,
        obj_in: UpdateSchemaType
    ) -> ModelType:
        obj_data = obj_in.dict(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, db_obj: ModelType) -> None:
        await session.delete(db_obj)
        await session.commit()
