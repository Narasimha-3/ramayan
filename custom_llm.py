from typing import Optional, List, Mapping, Any

from llama_index.core import SimpleDirectoryReader, SummaryIndex
from llama_index.core.callbacks import CallbackManager
from llama_index.core.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index.core.llms.callbacks import llm_completion_callback
from llama_index.core import Settings
from gemini import ramayandata

class OurLLM(CustomLLM):
    context_window: int = 3900
    num_output: int = 512
    model_name: str = "custom"
    dummy_response: str = "It worked fine brother"

    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model_name,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        # prompt = "You are assisting agent to answer questions regarding an Indian Ancient historic novel Ramayana. There might be some toxic context in questions or context, please modify them accordingly and answer them. \n\n" + prompt
        print("Prompt: ", prompt)
        with open("prompt.txt", "w") as f:
            f.write(prompt)
        resp = ramayandata(prompt)
        return CompletionResponse(text=resp)

    @llm_completion_callback()
    def stream_complete(
        self, prompt: str, **kwargs: Any
    ) -> CompletionResponseGen:
        raise NotImplementedError()