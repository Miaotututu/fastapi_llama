prompt_template1 = """
Please answer the user's question based on the database selected by the user and some of the available table structure definitions of the database.
Database name:{0}, Table structure definition: {1}
Constraint:1.Please understand the user's intention based on the user's question, and use the given table structure definition to create a grammatically correct mysql sql. If sql is not required, answer the user's question directly.
2.Always limit the query to a maximum of 50 results unless the user specifies in the question the specific number of rows of data he wishes to obtain.
3.You can only use the tables provided in the table structure information to generate sql. If you cannot generate sql based on the provided table structure, please say: "The table structure information provided is not enough to generate sql queries." It is prohibited to fabricate information at will.
4.Please be careful not to mistake the relationship between tables and columns when generating SQL.
5.Please check the correctness of the SQL and ensure that the query performance is optimized under correct conditions.
User Question:{2}
Please think step by step and SQL Query to run
"""
