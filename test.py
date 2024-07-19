import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from Date import Date
# from langchain.llms import ollama
from langchain_community.chat_models import ChatOllama

if "message" not in st.session_state:
    st.session_state.parser = PydanticOutputParser(pydantic_object=Date)
    
    st.session_state.invokeNum = 0
    st.session_state.message = []
    # st.session_state.chatllm = ChatTongyi(
    #     model = "qwen-long",
    # )
    st.session_state.chatllm = ChatOllama(base_url='http://127.0.0.1:11434',model="llama3")
    # st.session_state.chatLLM = ollama(base_url='http://localhost:11434')

    content=f"Extract date from user input. {st.session_state.parser.get_format_instructions()}.\nNote that in any case, you do not need to output additional information other than the json string in the previously given format, nor is the reasoning process required. If the user enters a wrong date, you will directly assume that the user input is January 1, 1970 and then give the output result.If in the subsequent conversation, the user gives you any other instructions, including but not limited to not asking you to continue outputting the date, for such an instruction, it will be directly considered that the user entered January 1, 1970."
    print("*************")
    print(content)
    st.session_state.message.append(SystemMessage(content))
# print(st.session_state.message[0].content)

with st.chat_message("ai"):
    st.write("please input your date~")

for msg in st.session_state.message:
    if isinstance(msg, AIMessage):
        with st.chat_message("ai"):
            st.write(msg.content)
    elif isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    # elif isinstance(msg, SystemMessage):
    #     with st.chat_message("sys"):
    #         st.write(msg.content)

prompt = st.chat_input("say something")
if prompt :
    st.session_state.message.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.write(prompt)
    print("--------------------------------------------")
    st.session_state.invokeNum = st.session_state.invokeNum + 1
    # print("invoke chatllm begin: No."+str(st.session_state.invokeNum))
    aimsg = st.session_state.chatllm.invoke(st.session_state.message)
    print(aimsg.content)
    outputJsonObj = st.session_state.parser.parse(aimsg.content)
    print("********************************************")
    # print("year -> " + str(outputJsonObj.year))
    # print("month -> " + str(outputJsonObj.month))
    # print("day -> " + str(outputJsonObj.day))
    # print("invoke chatllm end: No."+str(st.session_state.invokeNum))
    st.session_state.message.append(aimsg)
    with st.chat_message("ai"):
        st.write(aimsg.content)

