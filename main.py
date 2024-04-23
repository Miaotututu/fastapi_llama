from fastapi import FastAPI
from pydantic import BaseModel
from database.mysql_op import get_table_row, get_path_curr, list_table, get_foreign_key, exe_select_sql
from chatWithModel.chatToSql import get_sql, QuestionResponse
from chatWithModel.llm import Text2sql_llama

app = FastAPI()


class Question(BaseModel):
    db_name: str
    user_question: str = None


class Answer(BaseModel):
    result: str
    db_result_list: list


# 调用本地微调模型
@app.post("/getSqlAnswer")
def get_answer(question: Question):
    result = get_sql(question.user_question, question.db_name)
    return Answer(result=result)


# 使用LLM类
@app.post("/getLLAMA")
def get_llama_answer(question: Question):
    llm = Text2sql_llama()
    result = llm(question.user_question)
    print(result)
    return result
