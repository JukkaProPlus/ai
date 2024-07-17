from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.tools import  render_text_description
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from AIOutput import AIOutput
from Tools1 import tools
from FuncDict import func_dict


parser = PydanticOutputParser(pydantic_object=AIOutput)

llm = ChatTongyi(model="qwen-long")
promptTemplate = PromptTemplate.from_file("./mySimpleAgent.txt")

instructions = parser.get_format_instructions()
prompt = promptTemplate.format(query="计算9和3的詹姆斯和", tools=render_text_description(tools), work_dir="./data/", instructions=instructions)
response = llm.invoke(prompt)
# print("***********************")
# print(response)
# print("#######################")
outputJsonObj = parser.parse(response.content)
# print(outputJsonObj.content)
# print(outputJsonObj.toolName)
# print(outputJsonObj.kwargs)

if outputJsonObj.toolName in func_dict:
    ans = func_dict[outputJsonObj.toolName](**outputJsonObj.kwargs)
    print(ans)
else:
    print("没有找到对应的工具")
