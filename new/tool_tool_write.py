from langchain.tools import StructuredTool
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_openai import ChatOpenAI
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
        inputToken = 0
        outputToken = 0
        totalToken = 0
        prompt = self.prompt.format(tools=render_text_description(tools), tool_desc=quest)
        message = []
        message.append(prompt)
        print(prompt)

        response = self.llm.invoke(message)
        message.append(response)
        print(f"本轮消耗的token数：inputToken:{response.response_metadata["token_usage"]["prompt_tokens"]}, outputToken:{response.response_metadata["token_usage"]["completion_tokens"]}, totalToken:{response.response_metadata["token_usage"]["total_tokens"]}")
        inputToken += response.response_metadata["token_usage"]["prompt_tokens"]
        outputToken += response.response_metadata["token_usage"]["completion_tokens"]
        totalToken += response.response_metadata["token_usage"]["total_tokens"]
        while True:
            if response.tool_calls and len(response.tool_calls) > 0:
                print("AAAAAAA "+ str(response))
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
                print("CCCCC "+ str(len(message)))
                response = self.llm.invoke(message)
                print(f"本轮消耗的token数：inputToken:{response.response_metadata["token_usage"]["prompt_tokens"]}, outputToken:{response.response_metadata["token_usage"]["completion_tokens"]}, totalToken:{response.response_metadata["token_usage"]["total_tokens"]}")
                inputToken += response.response_metadata["token_usage"]["prompt_tokens"]
                outputToken += response.response_metadata["token_usage"]["completion_tokens"]
                totalToken += response.response_metadata["token_usage"]["total_tokens"]
                message.append(response)
            else:
                print("BBBBB "+ str(response))
                print(f"本次运行总共消耗的token数：inputToken:{inputToken}, outputToken:{outputToken}, totalToken:{totalToken}")
                break



if __name__ == "__main__":
    print(1)
    prompt_file = "./prompts/ToolWriter.txt"
    prompt = PromptTemplate.from_template(read_file_with_chardet(prompt_file))
    # quest = "写一个斐波拉契数列的python代码,输入是一个整数n,输出是斐波拉契数列的前n个数组成的字符串,数之间用逗号分隔。"
    # quest = "写一个计算平方差的python工具,输入是一个两个数 a,b,输出为 'a和b的平方差是c'这样的字符串，这个字符串中的a和b是输入的参数，c是计算结果。"
    # quest = "写一个计算三角形的面积的公式,输入是三角形的底边长和高,输出是'三角形的面积是c'这样的字符串，这个字符串中的底边长和高是输入的参数，面积是计算结果。"
    # quest = "写一个计算平行四边形面积的工具，输入是底边长和高，输出是‘这个底边为a,高为b的平行四边形的面积是c’这样的字符串，字符串里面的a和b分别用底边长和高填充，c用它的面积填充"
    # quest = "写一个计算根据顶点的坐标来计算三角形的面积的工具,输入是a:(Xa,Ya),b:(Xb,Yb),c:(Xc,Yc),输出是‘这个三角形的面积是area’这样的字符串，字符串里面的area用它的面积填充"
    # quest = "写一个计算球体体积的工具，输入是半径r,输出是‘这个球的体积是V’这样的字符串，字符串里面的V用它的体积填充"
    # quest = "写一个计算四边形面积的工具，输入是a:(Xa,Ya),b:(Xb,Yb),c:(Xc,Yc),d:(Xd,Yd),输出是‘这个四边形的面积是area’这样的字符串，字符串里面的area用它的面积填充"
    # quest = "写一个能打印杨辉三角的工具，输入是n,输出是杨辉三角的前n行，每行用逗号分隔"
    # quest = "写一个能计算两个数的最大公约数的工具，输入是两个数a,b,输出是‘两个数的最大公约数是c’这样的字符串，字符串里面的c用它的最大公约数填充"
    quest = "写一个能计算两个数的最小公倍数的工具，输入时两个数a,b,输出时'a和b的最小公倍数是c'这样的字符串，字符串里面的a，b，c用对应的参数和结果填充"
    print(2)
    writer = PythonToolWriter(
        # llm=ChatTongyi(model="qwen-max"),
        llm=ChatOpenAI(model="gpt-4o-mini"),
        prompt_file="./prompts/ToolWriter1.txt"
    )
    print(3)
    writer.writeTool(quest)
    print(4)




# document_tool_tool_write = StructuredTool.from_function(
#     func=write_file,
#     name="write_file",
#     description="Write content to a file.",
# )
