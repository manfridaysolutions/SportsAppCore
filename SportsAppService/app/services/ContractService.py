from SportsAppModels.models.Contract import (
    Contract,
    ContractCreate,
    ContractUpdate,
)
from app.repositories.ContractRepository import ContractRepository
from app.services.BaseService import BaseService

class ContractService(BaseService[Contract, ContractCreate, ContractUpdate]):
    def __init__(self):
        super().__init__(ContractRepository())