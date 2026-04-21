from SportsAppModels.models.SportCategory import (
    SportCategory,
    SportCategoryCreate,
    SportCategoryUpdate,
    SportCategoryRead
)
from app.services.SportCategoryService import SportCategoryService
from app.api.v1.endpoints.BaseEndpoint import BaseEndpoint


sport_category_service = SportCategoryService()

sport_category_endpoint = BaseEndpoint[
    SportCategory,
    SportCategoryCreate,
    SportCategoryUpdate,
    SportCategoryRead
](
    service=sport_category_service,
    model_read=SportCategoryRead,
    prefix="/sport-categories",
    tags=["Sport Categories"]
).router
