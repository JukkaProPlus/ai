from langchain_core.pydantic_v1 import BaseModel, Field

class AIOutput(BaseModel):
    """大模型回复的对象"""
    content: str = Field(..., description="你想要回复的内容")
    toolName: str = Field(..., description="你想要使用的工具的名字")
    kwargs: dict = Field(..., description="字典形式的参数，传递给你想要调用的工具")
