from SportsAppModels.models.StatDefinition import (
    StatDefinition,
    StatDefinitionCreate,
    StatDefinitionUpdate,
    StatDefinitionRead
)

from app.services.StatDefinitonService import StatDefinitionService
from app.api.v1.endpoints.BaseEndpoint import BaseEndpoint

statDefinition_service = StatDefinitionService()

statDefinition_endpoint = BaseEndpoint[
    StatDefinition,
    StatDefinitionCreate,
    StatDefinitionUpdate,
    StatDefinitionRead
](
    service=statDefinition_service,
    model_create=StatDefinitionCreate,
    model_read=StatDefinitionRead,
    model_update=StatDefinitionUpdate,
    prefix="/statDefinition",
    tags=["StatDefinition"]
).router
