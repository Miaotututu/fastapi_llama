from pydantic import BaseModel
from typing import Dict

class DatabaseSettings(BaseModel):
    host: str
    port: int
    username: str
    password: str
    database_name: str

class MySettings(BaseModel):
    app_name: str = "MyApp"
    debug: bool = False
    databases: Dict[str, DatabaseSettings]


# 初始化设置
settings = MySettings(
    databases={
        "newData_mysql": DatabaseSettings(
            host="localhost",
            port=3306,
            username="user",
            password="password",
            database_name="my_database"
        ),
        "Golang_oracle": DatabaseSettings(
            host="remotehost",
            port=5432,
            username="user",
            password="password",
            database_name="another_database"
        ),
        "dimp_mysql": DatabaseSettings(
            host="remotehost",
            port=5432,
            username="user",
            password="password",
            database_name="another_database"
        ),
        "twshop_oracle": DatabaseSettings(
            host="remotehost",
            port=5432,
            username="user",
            password="password",
            database_name="another_database"
        )
    }
)

