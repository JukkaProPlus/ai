import re
from typing import Union
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.tools import StructuredTool
from langchain_core.language_models import BaseChatModel, BaseLanguageModel
from langchain_core.output_parsers import BaseOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate

# from Models.Factory import ChatModelFactory
from ColoredPrintHandlers import ColoredPrintHandler
# from Utils.PrintUtils import CODE_COLOR
from langchain_openai import ChatOpenAI
from ExcelTool import get_first_n_rows, get_column_names
from langchain_experimental.utilities import PythonREPL


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


class ExcelAnalyser:
    """
    通过程序脚本分析一个结构化文件（例如excel文件）的内容。
    输人中必须包含文件的完整路径和具体分析方式和分析依据，阈值常量等。
    """

    def __init__(
            self,
            llm: Union[BaseLanguageModel, BaseChatModel],
            prompt_file="./excel_analyser.txt",
            verbose=False
    ):
        self.llm = llm
        self.prompt = PromptTemplate.from_file(prompt_file)
        self.verbose = verbose
        self.verbose_handler = ColoredPrintHandler()

    def analyse(self, query, filename):

        """分析一个结构化文件（例如excel文件）的内容。"""

        # columns = get_column_names(filename)
        inspections = get_first_n_rows(filename, 3)
        print("***************inspections***************** A")
        print(inspections)
        print("***************inspections***************** B")
        code_parser = PythonCodeParser()
        chain = self.prompt | self.llm | StrOutputParser()

        response = ""

        for c in chain.stream({
            "query": query,
            "filename": filename,
            "inspections": inspections
        }, config={
            "callbacks": [
                self.verbose_handler
            ] if self.verbose else []
        }):
            response += c

        print("***************response***************** A")
        print(response)
        print("***************response***************** B")
        code = code_parser.parse(response)
        print("***************code***************** A")
        print(code)
        print("***************code***************** B")
        if code:
            ans = query+"\n"+PythonREPL().run(code)
            return ans
        else:
            return "没有找到可执行的Python代码"

    def as_tool(self):
        return StructuredTool.from_function(
            func=self.analyse,
            name="AnalyseExcel",
            description=self.__class__.__doc__.replace("\n", ""),
        )


if __name__ == "__main__":
    print(ExcelAnalyser(
        # ChatModelFactory.get_model("gpt-4o"),
        ChatTongyi(
            model = "qwen-max",
        )
    ).analyse(
        query="8月销售额",
        filename="./2023年8月-9月销售记录.xlsx"
    ))