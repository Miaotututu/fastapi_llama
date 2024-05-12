import requests


def get_dataSource_list():
    url = "http://0.0.0.0:6667/getDataSource"
    response = requests.post(url)
    if response.status_code != 200:
        return ["newData_mysql","Golang_oracle","dimp_mysql","twshop_oracle"]
    data = response.json()
    db_list = data["db_list"]

    return db_list

db_list = []
db_list = get_dataSource_list()

print(db_list)
print(type(db_list))