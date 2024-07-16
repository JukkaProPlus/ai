from langchain_core.prompts import PromptTemplate

# from Tools import tools

class FuncCaller():
    def __init__(self, llm, tools_desc: str):
        self.llm = llm
        self.tools_desc = tools_desc
        self.prompt = PromptTemplate.from_file("funcCallerPrompt.txt")
    def invoke(self, user_input: str):
        result = self.llm.invoke(self.prompt.format(tools_desc=self.tools_desc, user_input=user_input))
        return result

# from FileTool import *

# def run() -> str:
#     current_dir = getWorkDir789()
#     files = [f for f in getAllFilePath666(current_dir) if isFileExist123(f)]
#     result = "\n".join(files)
#     return result


# # def run():
# #     work_dir = getWorkDir789()
# #     files = [f for f in getAllFilePath666(work_dir) if isFileExist123(f)]
# #     return "\n".join(files)

# print(run())