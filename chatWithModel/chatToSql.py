from pydantic import BaseModel
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer

model_id = "/home/model_zoo/LLM/llama2/Llama-2-7b-hf/"

tokenizer = LlamaTokenizer.from_pretrained(model_id)

model = LlamaForCausalLM.from_pretrained(model_id, load_in_8bit=True, device_map='auto', torch_dtype=torch.float16)


class QuestionResponse(BaseModel):
    instruction: str
    sql: str
    result: list


# TODO
def get_sql(instruction, input_question):
    return "SELECT * FROM department";
