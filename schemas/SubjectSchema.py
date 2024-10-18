from typing import Optional
from pydantic import BaseModel, Field


class SubjectSchema(BaseModel):
    # define attributes or fields
    id: Optional[int] = None
    name: str = Field(min_length=1, max_length=150)
    description: Optional[str] = Field(min_length=1, max_length=300)

    # define schema example
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Mathematics",
                "description": "Mathematics is the study of quantity, structure, change, and space."
            }
        }