from FuncCaller import FuncCaller
from FuncTools import tools
from langchain_core.tools import  render_text_description

from langchain_community.chat_models.tongyi import ChatTongyi
chatllm = ChatTongyi(
        model = "qwen-long",
    )

caller = FuncCaller(chatllm, render_text_description(tools=tools))
response = caller.invoke("当前工作目录下有哪些文件？")
print("**********************************")
print(response.content)
print("**********************************")