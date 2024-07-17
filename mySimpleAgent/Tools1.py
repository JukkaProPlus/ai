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
document_getJamesSum_tool = StructuredTool.from_function(
    func=getJamesSum,
    name="getJamesSum",
    description=getJamesSum.__doc__,
)

tools = [
    document_getWorkDir_tool,
    document_isFileExist_tool,
    document_isDirExist_tool,
    document_getAllFilePath_tool,
    document_getJamesSum_tool,
    excelAnalysisTool(
        llm = ChatTongyi(model="qwen-max"),
        prompt=PromptTemplate.from_file("./mySimpleAgent.txt"),
    ).as_tool()
    ]

