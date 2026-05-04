from SportsAppModels.models.StatDefinition import (
    StatDefinition,
    StatDefinitionCreate,
    StatDefinitionUpdate,
)

from app.repositories.BaseRepository import BaseRepository

class StatDefinitionRepository(BaseRepository[
    StatDefinition,
    StatDefinitionCreate, 
    StatDefinitionUpdate
]):
    default_relationships = ["stat_unit"]  # Automatically load related categories

    def __init__(self):
        super().__init__(StatDefinition)