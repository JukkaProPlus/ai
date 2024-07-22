from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.tools import  render_text_description
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage
from AIOutput import AIOutput
from Tools1 import tools
from FuncDict import func_dict
import streamlit as st
from MsgType import MsgType
from FileTool import read_file_with_chardet

def recordMessage(msg, isFuncResult=False, isPaserseErrorReply=False):
    st.session_state.message.append(msg)
    if isinstance(msg, HumanMessage):
        if isPaserseErrorReply:
            st.session_state.messageType.append(MsgType.ASSISTANT_FAILED_REPLY)
        elif isFuncResult:
            st.session_state.messageType.append(MsgType.FUNCTION_RESULT)
        else:
            st.session_state.messageType.append(MsgType.USER)
    elif isinstance(msg, SystemMessage):
        st.session_state.messageType.append(MsgType.SYSTEM)
    elif isinstance(msg, AIMessage):
        try:
            outputJsonObj = st.session_state.parser.parse(msg.content)
            if outputJsonObj.toolName != "":
                #是函数调用
                st.session_state.messageType.append(MsgType.FUNCTION_CALL)
            else:
                #是普通回复
                st.session_state.messageType.append(MsgType.ASSISTANT)
        except:
            st.session_state.messageType.append(MsgType.ASSISTANT_FAILED)



if "message" not in st.session_state:
    print("init")
    st.session_state.invokeNum = 0
    st.session_state.parser = PydanticOutputParser(pydantic_object=AIOutput)
    st.session_state.message = []
    st.session_state.messageType = []
    st.session_state.chatLLM = ChatTongyi(model="qwen-long")
    # st.session_state.chatLLM = ChatOllama(base_url='http://127.0.0.1:11434',model="llama3")
    # st.session_state.chatLLM = ChatOllama(base_url='http://127.0.0.1:11434',model="qwen2:7b")

    promptTemplate = PromptTemplate.from_template(read_file_with_chardet("./mySimpleAgent.txt"))
    # promptTemplate = PromptTemplate.from_file("./mySimpleAgent.txt")
    instructions = st.session_state.parser.get_format_instructions()
    # print()
    prompt = promptTemplate.format(tools=render_text_description(tools), work_dir="./data/", instructions=instructions)
    sysMsg = SystemMessage(content=prompt)
    recordMessage(sysMsg)

for messageType, message in zip(st.session_state.messageType, st.session_state.message):
    if messageType == MsgType.SYSTEM:
        with st.chat_message(name="system", avatar="⚙️"):
            print("AAAAAAA"+message.content)
            st.write(message.content)
    elif messageType == MsgType.USER:
        with st.chat_message(name="user", avatar="🤵"):
            print("BBBBBB"+message.content)
            st.write(message.content)
    elif messageType == MsgType.ASSISTANT:
        # with st.chat_message(name="ai", avatar="🤖"):
        #     print("CCCCCC"+message.content)
        #     st.write(message.content)
        outputJsonObj = st.session_state.parser.parse(message.content)
        if outputJsonObj.content != "":
            if outputJsonObj.toolName != "":
                with st.chat_message(name="ai", avatar="🤖"):
                    st.write(f"我需要调用本地工具才能解答您的问题,工具名:{outputJsonObj.toolName}")
            else:
                with st.chat_message(name="ai", avatar="🤖"):
                    st.write(outputJsonObj.content)
    elif messageType == MsgType.FUNCTION_CALL:
        if message.content != "":
            with st.chat_message(name="ai", avatar="🤖"):
                outputJsonObj = st.session_state.parser.parse(message.content)
                print("DDDDDD"+message.content)
                st.write(f"我需要调用本地工具才能解答您的问题,工具名:{outputJsonObj.toolName}")

    elif messageType == MsgType.FUNCTION_RESULT:
        if message.content != "":
            with st.chat_message(name="tool", avatar="🔧"):
                print("EEEEEEE"+message.content)
                st.write(message.content)
    elif messageType == MsgType.ASSISTANT_FAILED:
        
        # HumanMessage(content="你回复的内容解析不了，请检查是否是严格按照前面规定的格式进行了回复，然后输出严格按照格式的回复")
        pass
        # with st.chat_message(name="ai", avatar="🤖"):
        #     print("FFFFFFFF"+message.content)
        #     st.write(message.content)


# # print(outputJsonObj.content)
# # print(outputJsonObj.toolName)
# # print(outputJsonObj.kwargs)

prompt = st.chat_input("请输入你的问题")
if prompt:
    print("***************用户输入begin***********************")
    print(prompt)
    print("***************用户输入返回end***********************")
    recordMessage(HumanMessage(content=prompt))
    # st.session_state.message.append(HumanMessage(content=prompt))
    # st.session_state.messageType.append(MsgType.USER)
    with st.chat_message(name="user", avatar="🤵"):
        print("FFFFFFF"+prompt)
        st.write(prompt)

    while True:
        st.session_state.invokeNum = st.session_state.invokeNum + 1
        print(f"invokeNum = {st.session_state.invokeNum}")
        response = st.session_state.chatLLM.invoke(st.session_state.message)
        print("***************AI返回begin***********************")
        print(response.content)
        print("***************AI返回end***********************")
        recordMessage(response)
        try:
            outputJsonObj = st.session_state.parser.parse(response.content)
            if outputJsonObj.content != "":
                if outputJsonObj.toolName != "":
                    with st.chat_message(name="ai", avatar="🤖"):
                        print(f"GGGGGGGG我需要调用本地工具才能解答您的问题,工具名:{outputJsonObj.toolName}")
                        st.write(f"我需要调用本地工具才能解答您的问题,工具名:{outputJsonObj.toolName}")
                else:
                    with st.chat_message(name="ai", avatar="🤖"):
                        print("HHHHHHHH"+outputJsonObj.content)
                        st.write(outputJsonObj.content)
            if outputJsonObj.toolName != "":
                if outputJsonObj.toolName in func_dict:
                    funcResult = func_dict[outputJsonObj.toolName](**outputJsonObj.kwargs)
                    funcResultMessage = HumanMessage(content=f"后面是调用本地工具{outputJsonObj.toolName}后的返回结果,不要对这个结果有任何质疑,根据这个结果按照规定的格式回答用户的问题就行了,结果是：{funcResult}")
                    print("****************工具返回begin**********************")
                    print(funcResultMessage.content)
                    print("****************工具返回end**********************")
                    recordMessage(funcResultMessage, isFuncResult=True)
                    with st.chat_message(name="tool", avatar="🔧"):
                        print("IIIIIIII"+funcResultMessage.content)
                        st.write(funcResultMessage.content)
                else:
                    funcResult = "没有找到对应的工具"
                    funcResultMessage = HumanMessage(content=f"{funcResult}:{outputJsonObj.toolName}")
                    print("****************工具返回begin**********************")
                    print(funcResultMessage.content)
                    print("****************工具返回end**********************")
                    recordMessage(funcResultMessage, isFuncResult=True)
                    with st.chat_message(name="tool", avatar="🔧"):
                        print("JJJJJJJ"+funcResultMessage.content)
                        st.write(funcResultMessage.content)
            else:
                break
        except Exception as e:
            print("解析错误 " + str(e))
            recordMessage(HumanMessage(content="你回复的内容解析不了，请检查是否是严格按照前面规定的格式进行了回复，然后输出严格按照格式的回复"), isPaserseErrorReply=True)



# 

# llm = ChatTongyi(model="qwen-long")
# promptTemplate = PromptTemplate.from_file("./mySimpleAgent.txt")

# instructions = st.session_state.parser.get_format_instructions()
# tools_desc = render_text_description(tools)
# print(f"tools_desc = \n{tools_desc}")
# prompt = promptTemplate.format(query="计算9和3的詹姆斯和", tools=tools_desc, work_dir="./data/", instructions=instructions)
# response = llm.invoke(prompt)
# # print("***********************")
# # print(response)
# # print("#######################")
# outputJsonObj = st.session_state.parser.parse(response.content)
# # print(outputJsonObj.content)
# # print(outputJsonObj.toolName)
# # print(outputJsonObj.kwargs)

# if outputJsonObj.toolName in func_dict:
#     ans = func_dict[outputJsonObj.toolName](**outputJsonObj.kwargs)
#     print(ans)
# else:
#     print("没有找到对应的工具")
