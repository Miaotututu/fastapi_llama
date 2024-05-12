"""
直接调用本地微调模型demo
"""
from pydantic import BaseModel
import torch
from transformers import LlamaTokenizer, LlamaForCausalLM
from chatWithModel.prompt.prompt_template import prompt_template1, RESPONSE_FORMAT_SIMPLE
from database.mysql_op import get_table_info_list
import json

model_path = "/root/autodl-fs/CodeLlama-13b-CSpider-sql-sft-epoch2"
tokenizer = LlamaTokenizer.from_pretrained(model_path)
model = LlamaForCausalLM.from_pretrained(model_path, load_in_8bit=True, device_map='auto', torch_dtype=torch.float16)


class QuestionResponse(BaseModel):
    instruction: str
    sql: str
    result: list


def get_sql(user_question, db_name):
    table_info_list = get_table_info_list(db_name)
    prompt = prompt_template1.format(db_name, ",".join(table_info_list), user_question)
    print(prompt)
    model_input = tokenizer(prompt, return_tensors="pt").to("cuda")
    model.eval()
    with torch.no_grad():
        res = model.generate(**model_input, max_new_tokens=300)[0]
        result = tokenizer.decode(res, skip_special_tokens=True, spaces_between_special_tokens=False)
        print(type(result))
        sql = result.split("sql%_%")[-1]
        print(type(sql))
        print(sql)
        print("result is:" + result)
        return result, sql
