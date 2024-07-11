from langchain_core.pydantic_v1 import BaseModel, Field

class Date(BaseModel):
    """Date object."""
    year: int = Field(..., description="Year")
    month: int = Field(..., description="Month")
    day: int = Field(..., description="Day")