from langchain.tools import StructuredTool
from FileTool import *
from excelAnalysisTool import excelAnalysisTool
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts.prompt import PromptTemplate


document_getWorkDir_tool= StructuredTool.from_function(
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
document_getJamesResult_tool = StructuredTool.from_function(
    func=getJamesResult,
    name="getJamesResult",
    description=getJamesResult.__doc__,
)

document_getFileContent_tool = StructuredTool.from_function(
    func=getFileContent,
    name="getFileContent",
    description=getFileContent.__doc__,
)

tools = [
    document_getWorkDir_tool,
    document_isFileExist_tool,
    document_isDirExist_tool,
    document_getAllFilePath_tool,
    document_getJamesResult_tool,
    document_getFileContent_tool,
    excelAnalysisTool(
        llm = ChatTongyi(model="qwen-max"),
        prompt=PromptTemplate.from_file("./mySimpleAgent.txt"),
    ).as_tool()
    ]
