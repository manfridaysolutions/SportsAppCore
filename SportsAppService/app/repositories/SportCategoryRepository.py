from SportsAppModels.models.SportCategory import (
    SportCategory,
    SportCategoryCreate,
    SportCategoryUpdate
)

from app.repositories.BaseRepository import BaseRepository

class SportCategoryRepository(BaseRepository[
    SportCategory,
    SportCategoryCreate,
    SportCategoryUpdate
]):
    def __init__(self):
        super().__init__(SportCategory)
