prompt_template1 = """
Please answer the user's question based on the database selected by the user and some of the available table structure definitions of the database.
Database name:{0}, Table structure definition: {1}
Constraint:1.Please understand the user's intention based on the user's question, and use the given table structure definition to create a grammatically correct mysql sql. If sql is not required, answer the user's question directly.
2.Always limit the query to a maximum of 50 results unless the user specifies in the question the specific number of rows of data he wishes to obtain.
3.You can only use the tables provided in the table structure information to generate sql. If you cannot generate sql based on the provided table structure, please say: "The table structure information provided is not enough to generate sql queries." It is prohibited to fabricate information at will.
4.Please be careful not to mistake the relationship between tables and columns when generating SQL.
5.Please check the correctness of the SQL and ensure that the query performance is optimized under correct conditions.
6.Please choose the best one from the display methods given below for data rendering, and put the type name into the name parameter value that returns the required format. If you cannot find the most suitable one, use 'Table' as the display method. the available data display methods are as follows: response_line_chart:used to display comparative trend analysis data response_pie_chart:suitable for scenarios such as proportion and distribution statistics response_table:suitable for display with many display columns or non-numeric columns response_scatter_plot:Suitable for exploring relationships between variables, detecting outliers, etc. response_bubble_chart:Suitable for relationships between multiple variables, highlighting outliers or special situations, etc.
response_donut_chart:Suitable for hierarchical structure representation, category proportion display and highlighting key categories, etc.
response_area_chart:Suitable for visualization of time series data, comparison of multiple groups of data, analysis of data change trends, etc.
response_heatmap:Suitable for visual analysis of time series data, large-scale data sets, distribution of classified data, etc.
User Question:
    {2}
sql%_% 
"""

RESPONSE_FORMAT_SIMPLE = {
    "thoughts": "thoughts summary to say to user",
    "sql": "SQL Query to run",
    "display_type": "Data display method",
}