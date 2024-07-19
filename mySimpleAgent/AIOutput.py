from langchain_core.pydantic_v1 import BaseModel, Field

class AIOutput(BaseModel):
    """Rules your responses need to follow"""
    content: str = Field(..., description="The content you want to reply to, 'content' can only be a string, not any other content")
    toolName: str = Field(..., description="The name of the tool you want to use")
    kwargs: dict = Field(..., description="Parameters in dictionary form, passed to the tool you want to call")
