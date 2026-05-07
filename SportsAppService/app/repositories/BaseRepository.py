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

    async def _sync_relationships(self, session: AsyncSession, db_obj: ModelType, rel_data: dict):
        """
        Generic helper to sync list-based relationships (IDs to link objects).
        """
        mapper = inspect(self.model)
        relationships = mapper.relationships

        for field, incoming_ids in rel_data.items():
            rel_mapper = relationships[field]
            rel_model = rel_mapper.mapper.class_
            
            parent_pk_name = mapper.primary_key[0].name
            parent_id = getattr(db_obj, parent_pk_name)
            
            # Find the target ID key (e.g., 'sport_id')
            target_pk_name = [
                c.name for c in rel_mapper.mapper.primary_key 
                if c.name != parent_pk_name
            ][0]

            # Current state in DB
            current_rels = getattr(db_obj, field)
            current_lookup = {getattr(r, target_pk_name): r for r in current_rels}
            target_ids = set(incoming_ids)

            # 1. DELETE: Remove existing links not in the new set
            for rid, rel_obj in list(current_lookup.items()):
                if rid not in target_ids:
                    current_rels.remove(rel_obj)
                    await session.delete(rel_obj)

            # 2. INSERT: Add new links (skip if already exists)
            for rid in target_ids:
                if rid not in current_lookup:
                    # Parent ID may be None during initial create, SQLModel handles linking on add
                    params = {target_pk_name: rid}
                    if parent_id: 
                        params[parent_pk_name] = parent_id
                    
                    new_rel = rel_model(**params)
                    current_rels.append(new_rel)

    async def create(self, session: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        obj_data = obj_in.model_dump()
        mapper = inspect(self.model)
        
        # Separate relationships from standard data
        rel_data = {k: v for k, v in obj_data.items() if isinstance(v, list) and k in mapper.relationships}
        standard_data = {k: v for k, v in obj_data.items() if k not in rel_data}

        db_obj = self.model(**standard_data)
        session.add(db_obj)
        
        # Sync relationships (SQLModel handles the session linking)
        await self._sync_relationships(session, db_obj, rel_data)
        
        await session.commit()
        return await self.get_by_id(session, getattr(db_obj, mapper.primary_key[0].name))

    async def update(self, session: AsyncSession, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        obj_data = obj_in.model_dump(exclude_unset=True)
        mapper = inspect(self.model)
        
        # Separate data
        rel_data = {k: v for k, v in obj_data.items() if isinstance(v, list) and k in mapper.relationships}
        
        # Update standard fields
        for key, value in obj_data.items():
            if key not in rel_data and hasattr(db_obj, key):
                setattr(db_obj, key, value)

        # Sync relationships
        await self._sync_relationships(session, db_obj, rel_data)

        session.add(db_obj)
        await session.commit()
        return await self.get_by_id(session, getattr(db_obj, mapper.primary_key[0].name))

    async def delete(self, session: AsyncSession, id: int) -> bool:
        obj = await self.get_by_id(session, id)
        if not obj:
            return False
        await session.delete(obj)
        await session.commit()
        return True