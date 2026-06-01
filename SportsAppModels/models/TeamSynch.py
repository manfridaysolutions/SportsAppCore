from typing import Optional
from sqlmodel import SQLModel
# Assuming these are imported from your respective model locations
from .Team import TeamBase 
from .SourceDataMapping import SourceDataMappingCreate

class TeamSynch(TeamBase):
    source_data_mapping: Optional[SourceDataMappingCreate] = None