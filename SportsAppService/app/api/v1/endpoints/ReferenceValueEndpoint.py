from SportsAppModels.models.ReferenceValue import (
    ReferenceValue,
    ReferenceValueCreate,
    ReferenceValueUpdate,
    ReferenceValueRead
)
from app.services.ReferenceValueService import ReferenceValueService
from app.api.v1.endpoints.BaseEndpoint import BaseEndpoint


reference_value_service = ReferenceValueService()

reference_value_endpoint = BaseEndpoint[
    ReferenceValue,
    ReferenceValueCreate,
    ReferenceValueUpdate,
    ReferenceValueRead
](
    service=reference_value_service,
    model_read=ReferenceValueRead,
    model_update=ReferenceValueUpdate,
    prefix="/reference-values",
    tags=["Reference Values"]
).router
