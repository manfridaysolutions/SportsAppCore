from typing import Generic, TypeVar, Type, Optional, List
from sqlmodel import SQLModel, select, inspect
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    default_relationships: list = []

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_all(self, session: AsyncSession, **kwargs) -> List[ModelType]:
        statement = select(self.model)

        if self.default_relationships:
            for rel in self.default_relationships:
                prop = rel if not isinstance(rel, str) else getattr(self.model, rel)
                statement = statement.options(selectinload(prop))

        for key, value in kwargs.items():
            if value is not None and hasattr(self.model, key):
                attr = getattr(self.model, key)
                if not hasattr(attr, "type"):
                    continue

                target_value = value
                try:
                    python_type = getattr(attr.type, "python_type", None)
                    if python_type:
                        if python_type is bool and isinstance(value, str):
                            target_value = value.lower() in ("true", "1", "t", "y", "yes")
                        else:
                            target_value = python_type(value)
                except Exception:
                    target_value = value

                statement = statement.where(attr == target_value)           

        result = await session.exec(statement)
        return result.all()

    async def get_by_id(self, session: AsyncSession, id: int) -> Optional[ModelType]:
        mapper = inspect(self.model)
        pk_col = list(mapper.primary_key)[0]

        stmt = select(self.model).where(pk_col == id)

        if self.default_relationships:
            for rel in self.default_relationships:
                prop = rel if not isinstance(rel, str) else getattr(self.model, rel)
                stmt = stmt.options(selectinload(prop))

        result = await session.exec(stmt)
        return result.one_or_none()

    async def create(self, session: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        obj = self.model.model_validate(obj_in)
        session.add(obj)
        await session.commit()

        mapper = inspect(self.model)
        pk_name = mapper.primary_key[0].name
        return await self.get_by_id(session, getattr(obj, pk_name))

    async def update(
        self,
        session: AsyncSession,
        db_obj: ModelType,
        obj_in: UpdateSchemaType
    ) -> ModelType:
        obj_data = obj_in.model_dump(exclude_unset=True)
        mapper = inspect(self.model)
        relationships = mapper.relationships.keys()

        for field, value in obj_data.items():
            if field in relationships and isinstance(value, list):
                # --- Advanced Compare & Upsert Logic ---
                rel_mapper = mapper.relationships[field]
                rel_model = rel_mapper.mapper.class_
                current_items = getattr(db_obj, field)
                rel_pk = rel_mapper.mapper.primary_key[0].name 
                
                # 1. Map incoming items with IDs (Existing)
                new_data_lookup = {
                    item[rel_pk]: item 
                    for item in value 
                    if isinstance(item, dict) and item.get(rel_pk) is not None
                }
                
                # 2. Identify brand new items (No Primary Key)
                items_to_add = [
                    item for item in value 
                    if isinstance(item, dict) and item.get(rel_pk) is None
                ]
                
                current_ids = {getattr(item, rel_pk) for item in current_items}
                incoming_ids = set(new_data_lookup.keys())

                # 3. DELETE: Items in current DB state but NOT in incoming payload
                items_to_remove = [
                    item for item in current_items 
                    if getattr(item, rel_pk) not in incoming_ids
                ]
                for item in items_to_remove:
                    current_items.remove(item)
                    await session.delete(item)

                # 4. INSERT: Add the new items identified in Step 2
                for item_data in items_to_add:
                    new_rel_obj = rel_model.model_validate(item_data)
                    current_items.append(new_rel_obj)
                
                # 5. UPDATE: (Optional) Handle updates to existing relationship metadata here
                # Existing items in 'incoming_ids' are already in 'current_items',
                # so they remain untouched, satisfying your "no churn" requirement.

            else:
                # Standard Column Update
                setattr(db_obj, field, value)

        session.add(db_obj)
        await session.commit()
        
        pk_name = mapper.primary_key[0].name
        return await self.get_by_id(session, getattr(db_obj, pk_name))

    async def delete(self, session: AsyncSession, id: int) -> bool:
        obj = await self.get_by_id(session, id)
        if not obj:
            return False
        await session.delete(obj)
        await session.commit()
        return True