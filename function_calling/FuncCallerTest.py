from FuncCaller import FuncCaller
import sys
sys.path.append("./")
import re
# from FuncTools import tools
from FuncTools import *
from langchain_core.tools import  render_text_description
from langchain_experimental.utilities import PythonREPL
from langchain_core.output_parsers import BaseOutputParser, StrOutputParser

# ans = PythonREPL().run("""
# import os
# print(os.getcwd())
# """)
# print(ans)

class PythonCodeParser(BaseOutputParser):
    """从OpenAI返回的文本中提取Python代码。"""

    @staticmethod
    def __remove_marked_lines(input_str: str) -> str:
        lines = input_str.strip().split('\n')
        if lines and lines[0].strip().startswith('```'):
            del lines[0]
        if lines and lines[-1].strip().startswith('```'):
            del lines[-1]

        ans = '\n'.join(lines)
        return ans

    def parse(self, text: str) -> str:
        # 使用正则表达式找到所有的Python代码块
        python_code_blocks = re.findall(r'```python\n(.*?)\n```', text, re.DOTALL)
        # 从re返回结果提取出Python代码文本
        python_code = None
        if len(python_code_blocks) > 0:
            python_code = python_code_blocks[0]
            python_code = self.__remove_marked_lines(python_code)
        return python_code

from langchain_community.chat_models.tongyi import ChatTongyi
chatllm = ChatTongyi(
        model = "qwen-long",
    )

caller = FuncCaller(chatllm, render_text_description(tools=tools))
# response = caller.invoke("当前工作目录下有哪些文件？")
response = caller.invoke("当前工作目录是什么？")
# response = caller.invoke("打印一个helloworld")
print("**********************************")
print(response.content)
print("--------------------------------")
code_parser = PythonCodeParser()
code = code_parser.parse(response.content)
print(code)
print("+++++++++++++++++++++++++")

ans = PythonREPL().run(code)
print("^^^^^^^^^^^^^^^^^^^^^^^^")
print(ans)

print("**********************************")