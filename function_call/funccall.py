import streamlit as st
from langchain_community.chat_models import ChatTongyi
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
from langchain_core.messages import SystemMessage
from langchain_core.messages import ToolMessage

def GetWeatherFunc(location:str):
    if location == "长沙":
        return "长沙现在温度是23度"
    if location == "武汉":
        return "武汉现在温度是28度"
def GetPopulationFunc(location):
    if location == "长沙":
        return "长沙现有人口800万"
    if location == "武汉":
        return "武汉现有人口800万"
    

if "messages" not in st.session_state:
    print("init")
    st.session_state.messages = [
        SystemMessage("你是一个聊天机器人"),
    ]
    st.session_state.tongyi_chat = ChatTongyi(
        model="qwen-max",
        # top_p="...",
        # api_key="...",
        # other params...
    )
    class GetWeather(BaseModel):
        """获取指定城市的天气情况"""
        location:str = Field(
            ..., description="城市名字,如 '长沙'"
        )
    class GetPopulation(BaseModel):
        """获取指定城市的人口数量"""
        location:str = Field(
            ..., description="城市名字,如 '长沙'"
        )
    st.session_state.tongyi_chat_with_tool = st.session_state.tongyi_chat.bind_tools([GetWeather, GetPopulation])
for msg in st.session_state.messages:
    if isinstance(msg, AIMessage):
        with st.chat_message("ai"):
            st.write(msg.content)
    elif isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
if prompt := st.chat_input("say something"):
    st.session_state.messages.append(HumanMessage(prompt))
    with st.chat_message("user"):
        st.write(prompt)
    response = st.session_state.tongyi_chat_with_tool.invoke(st.session_state.messages)
    st.session_state.messages.append(AIMessage(response.content))

    print("*********************************")
    print(response)
    print(type(response))
    # if response.tool_calls and len(response.tool_calls):
    #     for caller in response.tool_calls:
    #         if caller["name"] == "GetWeather":
    #             st.session_state.messages.append(ToolMessage(content=GetWeatherFunc(caller["args"]["location"])),tool_call_id=response.id)
    #         if caller["name"] == "GetPopulation":
    #             st.session_state.messages.append(ToolMessage(content=GetPopulationFunc(caller["args"]["location"])),tool_call_id=response.id)
    #     st.session_state.tongyi_chat_with_tool.invoke(st.session_state.messages)
    if response.tool_calls and len(response.tool_calls):  
        for caller in response.tool_calls:  
            if caller["name"] == "GetWeather":  
                content = GetWeatherFunc(caller["args"]["location"])  
                tool_message = ToolMessage(content=content, tool_call_id=response.id)  # 注意这里如何创建 ToolMessage 实例  
                st.session_state.messages.append(tool_message)  
            elif caller["name"] == "GetPopulation":  # 使用 elif 而不是另一个 if，以避免不必要的检查  
                content = GetPopulationFunc(caller["args"]["location"])  
                tool_message = ToolMessage(content=content, tool_call_id=response.id)  
                st.session_state.messages.append(tool_message)  
        response = st.session_state.tongyi_chat_with_tool.invoke(st.session_state.messages)
        st.session_state.messages.append(AIMessage(response.content))
        with st.chat_message("ai"):
            st.write(response.content)
    else:
        # if responsetool_calls
        with st.chat_message("ai"):
            st.write(response.content)
