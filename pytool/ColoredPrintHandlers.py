from typing import Optional, Union, Any, Dict
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import GenerationChunk, ChatGenerationChunk, LLMResult

# from Utils.PrintUtils import *


class ColoredPrintHandler(BaseCallbackHandler):
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
    ) -> Any:
        print(token, end="")
        return token

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        print("\n", end="")
        return response

    def on_tool_end(self, output: Any, **kwargs: Any) -> Any:
        """Run when tool ends running."""
        print()
        print("\n[Tool Return]")
        print(output)
        return output

    @staticmethod
    def on_thought_start(index: int, **kwargs: Any) -> Any:
        """自定义事件，非继承自BaseCallbackHandler"""
        print(f"\n[Thought: {index}]")
        return index

