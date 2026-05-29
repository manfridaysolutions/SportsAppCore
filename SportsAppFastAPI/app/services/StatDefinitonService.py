from SportsAppModels.models.StatDefinition import (
    StatDefinition,
    StatDefinitionCreate,
    StatDefinitionUpdate,
)
from app.repositories.StatDefinitionRepository import StatDefinitionRepository
from app.services.BaseService import BaseService

class StatDefinitionService(BaseService[StatDefinition, StatDefinitionCreate, StatDefinitionUpdate]):
    def __init__(self):
        super().__init__(StatDefinitionRepository())