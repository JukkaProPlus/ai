from langchain.tools import StructuredTool
import pandas as pd
import re
from langchain_core.output_parsers import BaseOutputParser, StrOutputParser
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



def get_sheet_names(
        filename: str
) -> str:
    """获取 Excel 文件的工作表名称"""
    excel_file = pd.ExcelFile(filename)
    sheet_names = excel_file.sheet_names
    return f"这是 '{filename}' 文件的工作表名称：\n\n{sheet_names}"


def get_column_names(
        filename: str
) -> str:
    """获取 Excel 文件的列名"""

    # 读取 Excel 文件的第一个工作表
    df = pd.read_excel(filename, sheet_name=0)  # sheet_name=0 表示第一个工作表

    column_names = '\n'.join(
        df.columns.to_list()
    )
    result = f"这是 '{filename}' 文件第一个工作表的列名：\n\n{column_names}"
    return result

def get_first_n_rows(
        filename: str,
        n: int = 3
) -> str:
    """获取 Excel 文件的前 n 行"""

    result = get_sheet_names(filename) + "\n\n"

    result += get_column_names(filename) + "\n\n"

    # 读取 Excel 文件的第一个工作表
    df = pd.read_excel(filename, sheet_name=0)  # sheet_name=0 表示第一个工作表

    n_lines = '\n'.join(
        df.head(n).to_string(index=False, header=True).split('\n')
    )

    result += f"这是 '{filename}' 文件第一个工作表的前{n}行样例：\n\n{n_lines}"
    return result

class excelAnalysisTool:
    """
    通过程序脚本分析一个结构化文件（例如excel文件）的内容。
    输人中必须包含文件的完整路径和具体分析方式和分析依据，阈值常量等。
    """
    def __init__(self,llm, prompt):
        self.prompt=prompt
        self.llm=llm

    def invoke(self, excelFilePath, input):
        data = get_first_n_rows(excelFilePath)
        prompt = self.prompt.format(path=excelFilePath, data=data, input=input)
        ans = self.llm.invoke(prompt)
        print(ans)
        print("******************************************")
        code_parser = PythonCodeParser()
        pycode = code_parser.parse(ans.content)

        ans = input+"\n"+PythonREPL().run(pycode)
        print(ans)
        

    def as_tool(self):
        return StructuredTool.from_function(
            func=self.invoke,
            name="AnalyseExcel",
            description=self.__class__.__doc__.replace("\n", ""),
        )
    

if __name__ == "__main__":
    from langchain_community.chat_models.tongyi import ChatTongyi
    from langchain_core.prompts.prompt import PromptTemplate
    from FileTool import read_file_with_chardet
    tool1 = excelAnalysisTool(ChatTongyi(model="qwen-long"), prompt = PromptTemplate.from_template(read_file_with_chardet("./excelAnalysisTool.txt")))
    filePath = "./data/六年级一班期中考试成绩.xlsx"
    tool1.invoke(filePath, "总分最高的是谁？")