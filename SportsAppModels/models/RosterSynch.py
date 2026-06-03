from typing import List, Optional, Any
from sqlmodel import Field
from .Roster import RosterBase
from .Athlete import Athlete
from .SourceDataMapping import SourceDataMappingCreate

class RosterSynch(RosterBase, table=False):
    # Use 'Any' (capitalized) instead of 'any' (built-in function)
    # This acts as a placeholder for the roster position data coming from the MLB API
    roster_positions: List[Any] = []
    athlete: Athlete
    
    source_data_mapping: Optional[SourceDataMappingCreate] = None