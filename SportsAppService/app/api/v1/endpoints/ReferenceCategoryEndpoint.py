from typing import List

from SportsAppModels.models.ReferenceCategory import (
    ReferenceCategory,
    ReferenceCategoryCreate,
    ReferenceCategoryUpdate,
    ReferenceCategoryRead
)
from app.services.ReferenceCategoryService import ReferenceCategoryService
from app.api.v1.endpoints.BaseEndpoint import BaseEndpoint
from app.db.session import get_session

from fastapi import Query, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

reference_category_service = ReferenceCategoryService()

reference_category_endpoint = BaseEndpoint[
    ReferenceCategory,
    ReferenceCategoryCreate,
    ReferenceCategoryUpdate,
    ReferenceCategoryRead
](
    service=reference_category_service,
    model_read=ReferenceCategoryRead,
    model_update=ReferenceCategoryUpdate,
    prefix="/reference-categories",
    tags=["Reference Categories"]
).router

@reference_category_endpoint.get(
        "/by-names/", 
        response_model=List[ReferenceCategoryRead], summary="Get Reference Categories by Names")

async def get_categories_by_names(
    # names: Optional[List[str]] = Query(None)
    names: List[str] = Query(..., description="List of category names to filter by"),
    session: AsyncSession = Depends(get_session)
):
    
    return await reference_category_service.get_by_names(session, names)