from SportsAppModels.models.Contract import (
    Contract,
    ContractCreate,
    ContractUpdate,
)

from app.repositories.BaseRepository import BaseRepository

class ContractRepository(BaseRepository[Contract, ContractCreate, ContractUpdate]):
    default_relationships = ["athlete", "team", "start_season", "end_season"]

    def __init__(self):
        super().__init__(Contract)