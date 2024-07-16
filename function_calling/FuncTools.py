from langchain.tools import StructuredTool
from FileTool import *

document_getWorkDir_tool = StructuredTool.from_function(
    func=getWorkDir,
    name="getWorkDir",
    description=getWorkDir.__doc__,
)
document_isFileExist_tool = StructuredTool.from_function(
    func=isFileExist,
    name="isFileExist",
    description=isFileExist.__doc__,
)
document_isDirExist_tool = StructuredTool.from_function(
    func=isDirExist,
    name="isDirExist",
    description=isDirExist.__doc__,
)
document_getAllFilePath_tool = StructuredTool.from_function(
    func=getAllFilePath,
    name="getAllFilePath",
    description=getAllFilePath.__doc__,
)

tools = [
    document_getWorkDir_tool,
    document_isFileExist_tool,
    document_isDirExist_tool,
    document_getAllFilePath_tool,
]
