from SportsAppModels.models.ReferenceValue import (
    ReferenceValue,
    ReferenceValueCreate,
    ReferenceValueUpdate
)
from app.repositories.ReferenceValueRepository import ReferenceValueRepository
from app.services.BaseService import BaseService

class ReferenceValueService(BaseService[
    ReferenceValue,
    ReferenceValueCreate,
    ReferenceValueUpdate
]):
    def __init__(self):
        super().__init__(ReferenceValueRepository())