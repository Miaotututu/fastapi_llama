"""
封装成一个LLM类后调用的demo
"""
from langchain.llms.base import LLM
from typing import Any, List, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from transformers import LlamaTokenizer, LlamaForCausalLM
import torch

model_path = "/root/autodl-fs/CodeLlama-13b-CSpider-sql-sft-epoch2"


class Text2sql_llama(LLM):
    # 基于本地 InternLM 自定义 LLM 类
    tokenizer: LlamaTokenizer = None
    model: LlamaForCausalLM = None

    def __init__(self):
        # model_path: InternLM 模型路径
        # 从本地初始化模型
        super().__init__()
        print("正在从本地加载模型...")
        self.tokenizer = LlamaTokenizer.from_pretrained(model_path)
        self.model = LlamaForCausalLM.from_pretrained(model_path, load_in_8bit=True, device_map='auto',
                                                      torch_dtype=torch.float16)
        self.model = self.model.eval()
        print("完成本地模型的加载")

    def _call(self, prompt: str, stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any):
        # 重写调用函数
        system_prompt = """
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        """

        messages = [(system_prompt, '')]
        response, history = self.model.chat(self.tokenizer, prompt, history=messages)
        return response

    @property
    def _llm_type(self) -> str:
        return "Text2sql_llama"
