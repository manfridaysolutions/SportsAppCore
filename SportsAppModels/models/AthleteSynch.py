from typing import Optional
from sqlmodel import SQLModel
# Assuming these are imported from your respective model locations
from .Athlete import AthleteBase 
from .SourceDataMapping import SourceDataMappingCreate

class AthleteSynch(AthleteBase):
    source_data_mapping: Optional[SourceDataMappingCreate] = None