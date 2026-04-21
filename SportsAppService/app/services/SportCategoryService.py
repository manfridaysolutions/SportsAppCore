from SportsAppModels.models.SportCategory import (
    SportCategory,
    SportCategoryCreate,
    SportCategoryUpdate
)
from app.repositories.SportCategoryRepository import SportCategoryRepository
from app.services.BaseService import BaseService

class SportCategoryService(BaseService[
    SportCategory,
    SportCategoryCreate,
    SportCategoryUpdate
]):
    def __init__(self):
        super().__init__(SportCategoryRepository())