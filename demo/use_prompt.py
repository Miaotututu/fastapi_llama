"""
使用提示词来与大模型对话，引导返回需要的内容
"""
from transformers import LlamaTokenizer, LlamaForCausalLM, GenerationConfig, pipeline
from langchain.llms import HuggingFacePipeline
import torch
from langchain.prompts import (
    ChatPromptTemplate,
)
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

local_model_path = "/root/autodl-fs/CodeLlama-13b-CSpider-sql-sft-epoch2"

tokenizer = LlamaTokenizer.from_pretrained(local_model_path)

base_model = LlamaForCausalLM.from_pretrained(
    local_model_path,
    load_in_8bit=True,
    device_map='auto',
    torch_dtype=torch.float16
)

pipe = pipeline(
    "text-generation",
    model=base_model,
    tokenizer=tokenizer,
    max_length=1300,
)

local_llm = HuggingFacePipeline(pipeline=pipe)

output_template = """
Please answer the user's question based on the database selected by the user and some of the available table structure definitions of the database.
Database name:dimp, Table structure definition:  audit_log(id, action, oss_filename, project_name, status, task_status, table_name, node_id, table_cname, default_partition_value, custom_partition_value, partition_value, file_size, row_count, create_user, update_user, create_datetime, update_datetime, error_msg, rsvst1, rsvst2, rsvst3, rsvst4, rsvst5, rsvdc1, rsvdc2, rsvdc3, rsvdc4, rsvdc5). , auth_audit_log(id, project_id, table_name, assignee, create_user, update_user, create_datetime, update_datetime). , biz_module(id, project_name, biz_module, biz_module_cname, create_user, update_user, create_datetime, update_datetime). , department(dept_id, dept_name, create_user, update_user, create_datetime, update_datetime, dept_english_name). , mc_project(id, project_name, project_id, create_user, update_user, create_datetime, update_datetime). , mc_table(id, project_id, project_name, table_model_id, partition_type, table_name, table_cname, table_comment, table_lifecycle, partition_lifecycle, virtual_node_id, dept_id, biz_module_id, biz_module_contact, biz_scenario, biz_indicator, biz_limit, biz_end_date, create_user, update_user, create_datetime, update_datetime, last_import_datetime, operate_status, owner). , mc_table_model(id, table_model, table_model_type, model_comment, table_lifecycle, partition_lifecycle, create_user, update_user, create_datetime, update_datetime). , oss_audit_log(id, action, oss_file_name, status, create_user, update_user, create_datetime, update_datetime, error_msg). , role_menu(id, role, menu, create_user, update_user, create_datetime, update_datetime, rsvst1, rsvst2, rsvst3, rsvst4, rsvst5, rsvdc1, rsvdc2, rsvdc3, rsvdc4, rsvdc5). , user_project_table(id, user_id, table_name, project_id, create_user, update_user, create_datetime, update_datetime, rsvst1, rsvst2, rsvst3, rsvst4, rsvst5, rsvdc1, rsvdc2, rsvdc3, rsvdc4, rsvdc5). 
Constraint:1.Please understand the user's intention based on the user's question, and use the given table structure definition to create a grammatically correct mysql sql. If sql is not required, answer the user's question directly.
2.Always limit the query to a maximum of 50 results unless the user specifies in the question the specific number of rows of data he wishes to obtain.
3.You can only use the tables provided in the table structure information to generate sql. If you cannot generate sql based on the provided table structure, please say: "The table structure information provided is not enough to generate sql queries." It is prohibited to fabricate information at will.
4.Please be careful not to mistake the relationship between tables and columns when generating SQL.
5.Please check the correctness of the SQL and ensure that the query performance is optimized under correct conditions.
6.Please choose the best one from the display methods given below for data rendering, and put the type name into the name parameter value that returns the required format. If you cannot find the most suitable one, use 'Table' as the display method. the available data display methods are as follows: response_line_chart:used to display comparative trend analysis data response_pie_chart:suitable for scenarios such as proportion and distribution statistics response_table:suitable for display with many display columns or non-numeric columns response_scatter_plot:Suitable for exploring relationships between variables, detecting outliers, etc. response_bubble_chart:Suitable for relationships between multiple variables, highlighting outliers or special situations, etc.
response_donut_chart:Suitable for hierarchical structure representation, category proportion display and highlighting key categories, etc.
response_area_chart:Suitable for visualization of time series data, comparison of multiple groups of data, analysis of data change trends, etc.
response_heatmap:Suitable for visual analysis of time series data, large-scale data sets, distribution of classified data, etc.
user question:{question}

please extract following information:
thoughts: thoughts summary to say to user,
sql: SQL Query to run,
display_type: Data display method,
Format the response as JSON with the following keys:
thoughts
sql
display_type

"""

response_schemas = [
    ResponseSchema(name="thoughts", description="thoughts summary to say to user"),
    ResponseSchema(name="sql", description="SQL Query to run"),
    ResponseSchema(name="display_type", description="Data display method")
]

parser = StructuredOutputParser.from_response_schemas(response_schemas)

prompt_temp = ChatPromptTemplate.from_template(output_template)

user_question = "查询mc_table表中最新的一条记录"

messages = prompt_temp.format_messages(question=user_question, format_instructions=parser)

response = local_llm.invoke(messages)

print("response:  ")
print(response)
