from SportsAppModels.models.ReferenceCategory import (
    ReferenceCategory,
    ReferenceCategoryCreate,
    ReferenceCategoryUpdate
)
from app.repositories.ReferenceCategoryRepository import ReferenceCategoryRepository
from app.services.BaseService import BaseService

class ReferenceCategoryService(BaseService[
    ReferenceCategory,
    ReferenceCategoryCreate,
    ReferenceCategoryUpdate
]):
    def __init__(self):
        super().__init__(ReferenceCategoryRepository())