from SportsAppModels.models.ReferenceCategory import (
    ReferenceCategory,
    ReferenceCategoryCreate,
    ReferenceCategoryUpdate
)

from app.repositories.BaseRepository import BaseRepository

class ReferenceCategoryRepository(BaseRepository[
    ReferenceCategory,
    ReferenceCategoryCreate,
    ReferenceCategoryUpdate
]):
    default_relationships = ["reference_values"]  # Automatically load related categories

    def __init__(self):
        super().__init__(ReferenceCategory)
