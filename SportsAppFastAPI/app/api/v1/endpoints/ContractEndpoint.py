from typing import List

from SportsAppModels.models.Contract import (
    Contract,
    ContractCreate,
    ContractRead,
    ContractUpdate
)

from app.services.ContractService import ContractService
from app.api.v1.endpoints.BaseEndpoint import BaseEndpoint

from app.db.session import get_session

from fastapi import Query, Depends
from sqlmodel.ext.asyncio.session import AsyncSession


contract_service = ContractService()

contract_endpoint = BaseEndpoint[
    Contract,
    ContractCreate,
    ContractRead,
    ContractUpdate,
](
    service=contract_service,
    model_create=ContractCreate,
    model_read=ContractRead,
    model_update=ContractUpdate,
    prefix="/contract",
    tags=["Contract"]
).router