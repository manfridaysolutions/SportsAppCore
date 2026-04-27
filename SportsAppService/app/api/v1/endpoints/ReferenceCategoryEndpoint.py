from SportsAppModels.models.ReferenceCategory import (
    ReferenceCategory,
    ReferenceCategoryCreate,
    ReferenceCategoryUpdate,
    ReferenceCategoryRead
)
from app.services.ReferenceCategoryService import ReferenceCategoryService
from app.api.v1.endpoints.BaseEndpoint import BaseEndpoint


reference_category_service = ReferenceCategoryService()

reference_category_endpoint = BaseEndpoint[
    ReferenceCategory,
    ReferenceCategoryCreate,
    ReferenceCategoryUpdate,
    ReferenceCategoryRead
](
    service=reference_category_service,
    model_read=ReferenceCategoryRead,
    prefix="/reference-categories",
    tags=["Reference Categories"]
).router
