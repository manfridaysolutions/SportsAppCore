from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, UniqueConstraint

class SourceDataMappingBase(SQLModel):
    """
    Shared fields across all layers. Uses Optional with defaults 
    to maximize flexibility for database lookups and updates.
    """
    entity_type: Optional[str] = Field(default=None, nullable=False, max_length=50)
    internal_id: Optional[int] = Field(default=None, nullable=False)
    source_system: Optional[str] = Field(default=None, nullable=False, max_length=100)
    external_id: Optional[str] = Field(default=None, nullable=False, max_length=255)

class SourceDataMappingCreate(SourceDataMappingBase):
    """
    Strict validation schema for incoming API POST payloads.
    Guarantees that sync workers MUST provide all four fields.
    """
    entity_type: str = Field(..., max_length=50)
    source_system: str = Field(..., max_length=100)
    external_id: str = Field(..., max_length=255)

class SourceDataMappingUpdate(SourceDataMappingBase):
    pass

class SourceDataMapping(SourceDataMappingBase, table=True):
    """
    The actual PostgreSQL database table definition.
    """
    __tablename__ = "source_data_mapping"
    
    __table_args__ = (
        UniqueConstraint(
            "entity_type", 
            "source_system", 
            "external_id", 
            name="uq_entity_source_external"
        ),
        {"schema": "sports"},
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, 
        nullable=False
    )