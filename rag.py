import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from VectorDBConnector import MyVectorDBConnector
from Tools import *

dbConnector = MyVectorDBConnector(collection_name="demo_vec_rrf", embedding_fn=embedding_fn)
chatllm = ChatTongyi(model="qwen-long")
str = """
你是一个问答机器人, 你的任务是根据下述给定的已知信息回答用户的问题

已知信息:
{content}

用户的问题:
{question}

如果已知信息不包含用户问题的答案，或者已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。
请不要输出已知信息中不包含的信息或答案。
请用中文回答用户问题。
"""

prompt = PromptTemplate.from_template(str)

while True:
    question = input()
    content = dbConnector.search(query=question, top_n=2)
    docs = content["documents"]
    finalDocsStr = "\n\n".join(docs[0])
    finalPrompt = prompt.format(content=finalDocsStr, question=question)
    print("***********************************")
    print(finalPrompt)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    ans = chatllm.invoke(finalPrompt)
    print(ans.content)
