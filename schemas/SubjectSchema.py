from typing import Optional
from pydantic import BaseModel, Field, field_validator
from config.database import Session

from models.Subject import Subject


class SubjectSchema(BaseModel):
    ### SCHEMA PROPERTIES
    
    id: Optional[int] = None
    name: str = Field(min_length=1, max_length=150)
    description: Optional[str] = Field(min_length=1, max_length=300)

    ### VALIDATORS

    @field_validator("name")
    def name_must_be_unique(cls, value: str) -> str:
        # get db session
        db = Session()
        result = db.query(Subject).filter(Subject.name == value).count()
        if result:
            raise ValueError("Name must be unique")
        return value

    ### SCHEMA EXAMPLE

    # define schema example
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Mathematics",
                "description": "Mathematics is the study of quantity, structure, change, and space."
            }
        }