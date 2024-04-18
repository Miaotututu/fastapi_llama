import requests
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any

from langchain_community.llms.utils import enforce_stop_tokens
from langchain_core.callbacks import CallbackManagerForLLMRun


class Text2sql(LLM):
    history = []

    def __init__(self):
        super().__init__()

    @property
    def _llm_type(self) -> str:
        return "Text2sqlLLM"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        data = {'text': prompt}
        url = "http://0.0.0.0:6667/chat/"
        response = requests.post(url, json=data)
        if response.status_code != 200:
            return "error"
        resp = response.json()
        if stop is not None:
            response = enforce_stop_tokens(response, stop)
        self.history = self.history + [[None, resp['result']]]
        return resp['result']


llm = Text2sql()
llm("请给我一个查询mc_table表的sql")
