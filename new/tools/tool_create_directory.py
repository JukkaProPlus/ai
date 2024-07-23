import os
from langchain.tools import StructuredTool

def create_directory(directory_path: str) -> str:
    """创建指定的目录路径，返回创建结果。成功则返回'目录创建成功'，失败则返回错误信息。"""
    try:
        os.makedirs(directory_path, exist_ok=True)
        return "目录创建成功"
    except Exception as e:
        return f"创建目录时发生错误: {str(e)}"

# 将函数转换为StructuredTool并导出
document_tool_create_directory = StructuredTool.from_function(
    func=create_directory,
    name="CreateDirectory",
    description="根据提供的路径创建目录，返回创建结果。"
)