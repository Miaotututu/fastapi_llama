"""
一些常用的mysql操作
"""
import os

import pymysql

from .config.dev_config import settings


class MysqlDB(object):
    def __init__(self):
        try:
            self.con = pymysql.connect(
                host=settings.host,
                port=settings.port,
                user=settings.user,
                passwd=settings.password,
                db=settings.database,  # 数据库名
                charset='utf8'
            )
        except pymysql.Error as e:
            print("Error %d：%s" % (e.args[0], e.args[1]))
            exit()
        self.cursor = self.con.cursor()  # 创建游标对象

    # 增加信息
    def add_data(self, sql, data=[]):
        try:
            self.cursor.execute(sql, data)
            self.con.commit()
        except Exception as e:
            self.con.rollback()
            print("Error", e.args[0])

    # 修改或删除信息
    def update_or_delete(self, sql):
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as e:
            self.con.rollback()
            print("Error ", e.args[0])

    # 查询一条信息
    def search_one(self, sql):
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
        except Exception as e:
            return "Error " + e.args[0]
        return res

    def get_columns(self, sql):
        try:
            self.cursor.execute(sql)
            column_list = [tupleResult[0] for tupleResult in self.cursor.description]
        except Exception as e:
            return "Error " + e.args[0]
        return column_list

    def get_tables(self, sql):
        try:
            self.cursor.execute(sql)
            table_list = [tupleResult[0] for tupleResult in self.cursor.fetchall()]
            print(self.cursor)
        except Exception as e:
            return "Error " + e.args[0]
        return table_list

    # 查询全部信息
    def search_all(self, sql):
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
        except Exception as e:
            return "Error " + e.args[0]
        for r in res:
            yield r

    # 关闭游标和数据库的连接
    def __del__(self):
        self.cursor.close()
        self.con.close()


def get_pymysql_conn(host, user, password, db):
    return pymysql.connect(host=host, user=user, password=password, db=db, autocommit=True)


# 根据数据库名 拼接出一个提示词（弃用方案）
def get_table_row(db_name):
    instruction = (
        "I want you to act as a SQL terminal in front of an example database, you need only to return the sql "
        "command to me.Below is an instruction that describes a task, Write a response that appropriately "
        "completes the request.")

    table_list = list_table()
    table_list_str = ",".join(table_list)

    schema_table_info = "##Instruction:" + db_name + " contains tables such as " + table_list_str + "."

    table_col_info = ""
    for table in table_list:
        table_col_info += " Table {0} has columns such as {1}. ".format(table, ",".join(list_col(table)))

    foreign_key_info = ""
    for table in table_list:
        foreign_key_info += get_foreign_key(table)

    return instruction + schema_table_info + table_col_info + foreign_key_info


def get_path_curr():
    return os.path.dirname(__file__)


# 查询所有字段
def list_col(table_name):
    db = MysqlDB()
    column_list = db.get_columns("select * from %s" % table_name)
    return column_list


# 列出所有的表
def list_table():
    db = MysqlDB()
    table_list = db.get_tables("show tables")
    return table_list


# 获取表的外键
def get_foreign_key(table_name):
    db = MysqlDB()
    foreign_key_it = db.search_all(
        f"SELECT table_name, column_name, referenced_table_name, referenced_column_name FROM information_schema.key_column_usage WHERE constraint_name NOT LIKE '%FOREIGN KEY%' AND TABLE_NAME = '{table_name}' AND  REFERENCED_TABLE_NAME is not null")
    foreign_key_info = " "
    for tn, cn, rtn, rcn in foreign_key_it:
        foreign_key_info += " the {0} of {1} is the foreign key of {2} of {3}. ".format(cn, tn, rcn, rtn)
    return foreign_key_info


# 执行sql
def exe_select_sql(sql):
    db = MysqlDB()
    it = db.search_all(sql)

    result_list = []
    for item in it:
        result_list.append(list(item))
    return result_list


# 获取一个数据库中的所有表信息
def get_table_info_list():
    table_info_list = []
    table_list = list_table()
    for table in table_list:
        table_col_info = " {0}({1}). ".format(table, ", ".join(list_col(table)))
        table_info_list.append(table_col_info)
    return table_info_list
