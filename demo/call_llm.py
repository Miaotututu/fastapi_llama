"""
封装成LLM后调用的demo
"""
import requests
import json
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
        data = {"text": prompt,
               "db_name": "dimp",
               "user_question": prompt}
        print(data)
        url = "http://0.0.0.0:6667/getSqlAnswer"
        response = requests.post(url, data=json.dumps(data))
        if response.status_code != 200:
            return "error"
        resp = response.json()
        print(resp)
        if stop is not None:
            response = enforce_stop_tokens(response, stop)
        self.history = self.history + [[None, resp['result']]]
        return resp['result']


llm = Text2sql()
print("ready!!!")
print(llm("请给我一个查询mc_table表的sql"))
