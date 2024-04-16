from pydantic import BaseModel


class QuestionResponse(BaseModel):
    instruction: str
    sql: str
    result: list


# TODO
def get_sql(instruction, input_question):
    return "SELECT * FROM department";
