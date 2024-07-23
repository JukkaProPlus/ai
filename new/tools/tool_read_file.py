import chardet
from langchain.tools import StructuredTool
def read_file_with_chardet(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read()
def read_file(file_path):
    return read_file_with_chardet(file_path=file_path)

document_tool_read_file = StructuredTool.from_function(
    func=read_file,
    name="read_file",
    description="获取指定文件内容"
)
