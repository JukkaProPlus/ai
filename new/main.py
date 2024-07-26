import langchain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import GenerationChunk, ChatGenerationChunk, LLMResult
from uuid import UUID
from typing import Optional, Union, Any, Dict


from readFile import read_file_with_chardet
import importlib
import tools
# from langchain import langchain
# while True:
#     input()
#     importlib.reload(tools)
#     print(len(tools.tool_list))


llm = ChatOpenAI(model="gpt-4o-mini")
p = PromptTemplate.from_template("{input}")
# .format(input="hello,who are you?")
class Callback(BaseCallbackHandler):
    def __init__(self):
        BaseCallbackHandler.__init__(self)
    def on_llm_new_token(
            self,
            token: str,
            *,
            chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ):
        print(token, end="")
config = {
    "callbacks": [Callback()]
}
chain = p | llm | StrOutputParser()
for s in chain.stream(input= "hello,who are you?please do a detail self introduction.", config=config):
    # print(s, end="A")
    pass



