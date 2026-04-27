from SportsAppModels.models.ReferenceValue import (
    ReferenceValue,
    ReferenceValueCreate,
    ReferenceValueUpdate
)

from app.repositories.BaseRepository import BaseRepository

class ReferenceValueRepository(BaseRepository[
    ReferenceValue,
    ReferenceValueCreate,
    ReferenceValueUpdate
]):
    default_relationships = ["reference_category","sports"]  # Automatically load related categories

    def __init__(self):
        super().__init__(ReferenceValue)
