from langchain.tools import StructuredTool

class excelAnalysisTool:
    """
    通过程序脚本分析一个结构化文件（例如excel文件）的内容。
    输人中必须包含文件的完整路径和具体分析方式和分析依据，阈值常量等。
    """
    def __init__(self,llm, prompt, filepath):
        self.filepath=filepath
        self.prompt=prompt
        self.llm=llm

    def invoke(self,path, data, input):
        pass

    def as_tool(self):
        return StructuredTool.from_function(
            func=self.invoke,
            name="AnalyseExcel",
            description=self.__class__.__doc__.replace("\n", ""),
        )