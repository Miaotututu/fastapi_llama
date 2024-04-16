from pydantic import BaseConfig


class MysqlSettings(BaseConfig):
    database: str = "data_integration_management"
    user: str = "root"
    password: str = "200016lrz"
    host: str = "127.0.0.1"
    port: str = "3306"


# 实例化配置对象
settings = MysqlSettings()
