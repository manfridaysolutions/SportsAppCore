from datetime import datetime
from sqlmodel import SQLModel, Field


class SportCategoryBase(SQLModel):
    category_name: str = Field(index=True, nullable=False)
    description: str | None = Field(default=None)

class SportCategory(SportCategoryBase, table=True):
    __table_args__ = {"schema": "sports"}
    __tablename__ = "sport_categories"

    category_id: int | None = Field(default=None, primary_key=True)

class SportCategoryCreate(SportCategoryBase):
    pass


class SportCategoryRead(SportCategoryBase):
    category_id: int


class SportCategoryUpdate(SQLModel):
    category_name: str | None = None
    description: str | None = None
