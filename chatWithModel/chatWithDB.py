import json

from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from .jwt_token import generate_token


def get_glm(temperature):
    llm = ChatOpenAI(
        model_name="glm-4",
        openai_api_base="https://open.bigmodel.cn/api/paas/v4",
        openai_api_key=generate_token("c9013ab959212d97e15a990157aca180.Vnts9vS3PzWscsJm", 60),
        streaming=False,
        temperature=temperature
    )
    return llm


def get_schema(user_question):
    db_user = "root"
    db_password = "200016lrz"
    db_host = "127.0.0.1"
    db_name = "data_integration_management"
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

    agent_executor = create_sql_agent(get_glm(0.01), db=db, agent_type="openai-tools", verbose=True)

    output_template = """
    我需要你将下面的问题
    问题:{question}
    提取出下面的信息：
    table_names：这是一个字符串数组，里面包含需要查询的表
    table_schema：这是一个字符串数组，里面包含需要查询的表的sql_db_schema

    并将返回的内容以JSON的格式输出并且需要包含下面这些key：
    table_names
    table_schema

    {format_instructions}
    """
    response_schemas = [
        ResponseSchema(name="table_names", description="这是一个字符串数组，里面包含需要查询的表", type="List[string]"),
        ResponseSchema(name="table_schema", description="这是一个字符串数组，里面包含需要查询的表的sql_db_schema",
                       type="List[string]")]
    parser = StructuredOutputParser.from_response_schemas(response_schemas)

    prompt_temp = ChatPromptTemplate.from_template(output_template)

    messages = prompt_temp.format_messages(question=user_question, format_instructions=parser)

    response = agent_executor.invoke(messages)
    # agent_executor.invoke(
    #     "我想知道用户信息，我需要查询数据库的哪一些表？"
    # )
    print('response数据的type是')

    print(type(response))
    print('output数据的type是')
    print(type(response.get('output')))

    print('准备拿output数据')
    return response.get('output')
