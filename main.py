from fastapi import FastAPI
from pydantic import BaseModel
from database.mysql_op import get_table_row, get_path_curr, list_table, get_foreign_key, exe_select_sql
from chatWithModel.chatToSql import get_sql, QuestionResponse
from chatWithModel.llm import Text2sql_llama
from .database.config.db_info_config import settings

app = FastAPI()


class Question(BaseModel):
    db_name: str
    user_question: str = None


class Answer(BaseModel):
    result: str
    sql: str
    db_result: list

class db_list_response(BaseModel):
    db_list: list

# 调用本地微调模型
@app.post("/getSqlAnswer")
def get_answer(question: Question):
    result, sql = get_sql(question.user_question, question.db_name)
    db_result_list = exe_select_sql(question.db_name)
    return Answer(result='正确处理', sql=sql, db_result=db_result_list)


# 使用LLM类
@app.post("/getLLAMA")
def get_llama_answer(question: Question):
    llm = Text2sql_llama()
    result = llm(question.user_question)
    print(result)
    return result


@app.post("/getDataSource")
def get_data_source():
    print(settings.databases.keys())
    return db_list_response(db_list=settings.databases.keys())