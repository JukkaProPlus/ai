from langchain.tools import StructuredTool
import os
def list_dir(dir_path):
    return ",".join(os.listdir(dir_path))

document_tool_list_dir = StructuredTool.from_function(
    func=list_dir,
    name="list_dir",
    description="获取指定目录下所有文件名字"
)
