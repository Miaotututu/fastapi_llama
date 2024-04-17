from fastapi import FastAPI
from pydantic import BaseModel
from database.mysql_op import get_table_row, get_path_curr, list_table, get_foreign_key, exe_select_sql
from chatWithModel.chatToSql import get_sql, QuestionResponse

app = FastAPI()


class Question(BaseModel):
    db_name: str
    user_question: str = None


@app.post("/exeSQL")
def test_langchain_sql(question: Question):
    # 获取提示词
    instruction = get_table_row(question.db_name)
    question = question.user_question
    # 获取sql
    sql = get_sql(instruction, question)
    result = exe_select_sql(sql)

    qr = QuestionResponse(instruction=instruction, sql=sql, result=result)
    return qr.model_dump()


@app.post("/getRow")
def get_sql_row():
    return get_table_row("data_integration_management")


@app.post("/getpath")
def get_path():
    return get_path_curr()


@app.post("/getTables")
def get_tables():
    table_list = list_table()
    print(table_list)
    print(type(table_list))
    return table_list


@app.post("/getForeign")
def get_foreign():
    return get_foreign_key("audit_log")


@app.post("/getSqlAnswer")
def get_answer(question: Question):
    result = get_sql(question.user_question, question.db_name)
    return result
