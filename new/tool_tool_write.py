from langchain.tools import StructuredTool
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.language_models import BaseChatModel, BaseLanguageModel
from typing import Union
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import  render_text_description
from tools import tools
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
from langchain_core.messages import SystemMessage
from langchain_core.messages import ToolMessage
import chardet
def read_file_with_chardet(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read()


# def tool_write(file_path, content):
#     """Write content to a file."""
#     with open(file_path, 'w') as file:
#         file.write(content)


# def write_tool(quest):

class PythonToolWriter():
    def __init__(
            self,
            llm:Union[BaseLanguageModel, BaseChatModel],
            prompt_file = "./prompts/ToolWriter.txt"
        ):
        self.llm = llm.bind_tools(tools)
        self.prompt = PromptTemplate.from_template(read_file_with_chardet(prompt_file))
    def writeTool(self, quest):
        prompt = self.prompt.format(tools=render_text_description(tools), tool_desc=quest)
        message = []
        message.append(prompt)
        print(prompt)

        response = self.llm.invoke(message)
        message.append(response)
        print("AAAAAAA1 "+ str(response))
        while True:
            if response.tool_calls and len(response.tool_calls) > 0:
                for caller in response.tool_calls:
                    findTool = False
                    content = ""
                    for tool in tools:
                        if caller["name"] == tool.name:
                            findTool = True
                            print(f'caller["args"] = {caller["args"]}')
                            content = tool.func(**caller["args"])
                            print("content = "+str(content))
                    if findTool:
                        tool_message = ToolMessage(content=content, tool_call_id=caller["id"])
                        message.append(tool_message)
                    else:
                        tool_message = ToolMessage(content=f"没有找到工具{caller["name"]}", tool_call_id=caller["id"])
                        message.append(tool_message)
                response = self.llm.invoke(message)
                print("AAAAAAA2 "+ str(response))
            else:
                print("BBBBB "+ str(response))
                break



if __name__ == "__main__":
    print(1)
    prompt_file = "./prompts/ToolWriter.txt"
    prompt = PromptTemplate.from_template(read_file_with_chardet(prompt_file))
    # quest = "写一个斐波拉契数列的python代码,输入是一个整数n,输出是斐波拉契数列的前n个数组成的字符串,数之间用逗号分隔。"
    quest = "写一个计算平方差的python工具,输入是一个两个数 a,b,输出为 'a和b的平方差是c'这样的字符串，这个字符串中的a和b是输入的参数，c是计算结果。"
    print(2)
    writer = PythonToolWriter(
        llm=ChatTongyi(model="qwen-max"),
        prompt_file="./prompts/ToolWriter.txt"
    )
    print(3)
    writer.writeTool(quest)
    print(4)




# document_tool_tool_write = StructuredTool.from_function(
#     func=write_file,
#     name="write_file",
#     description="Write content to a file.",
# )
