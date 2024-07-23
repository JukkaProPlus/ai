from langchain.tools import StructuredTool
def write_file(file_path, content):
    """Write content to a file."""
    with open(file_path, 'w') as file:
        file.write(content)
    return "写入完毕"

document_tool_write_file = StructuredTool.from_function(
    func=write_file,
    name="write_file",
    description="Write content to a file.",
)
