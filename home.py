from langchain.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage

chatllm = ChatTongyi(
    model = "qwen-long",
)

prompt = PromptTemplate.from_template("你是一位资深的{career},请你基于你丰富的经验,回答用户的问题")


historyMsg = []
promptStr = prompt.format(career="程序员")
print("sys:"+promptStr)
historyMsg.append(SystemMessage(promptStr))
# promptStr1 = "你好，有什么可以帮助你？希望我的专业能力能够满足你的需求。"
# historyMsg.append(AIMessage(content=promptStr1))
# print("ai output:"+promptStr1)

while True:
    print("user input:", end="")
    userInpput = input()
    historyMsg.append(HumanMessage(userInpput))
    ans = chatllm.invoke(historyMsg)
    historyMsg.append(ans)
    print("ai output:",end="")
    print(ans.content)
    if userInpput == "再见" or userInpput == "拜拜" or userInpput == "bye" :
        break

