import gradio as gr
import requests
import json

block = gr.Blocks()


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


def big_model_chat(input_question, history,db_source):
    history = history or []
    s = list(sum(history, ()))
    s.append(input_question)
    data = {
            "db_name": "dimp",
            "user_question": input_question}

    print("111111")
    print(db_source)
    # url = "http://0.0.0.0:6667/getDataSource"
    # response = requests.post(url, data=json.dumps(data))
    # if response.status_code != 200:
    #     return "error"
    # resp = response.content.decode('utf-8')
    resp = "1+2+3+4+5"+db_source
    history.append((input_question, resp))
    return history, history


with block:
    with gr.Row():
        db_source = gr.Dropdown(db_list, label="data_source")

with block:
    gr.Markdown("""<h1><center>DataQueryAI-SQLTune1.0</center></h1>
    """)
    chatbot = gr.Chatbot()
    message = gr.Textbox()
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(big_model_chat, inputs=[message, state, db_source], outputs=[chatbot, state])

gr.close_all()  # 关闭所有正在运行的端口
block.launch(debug=True, share=True, server_port=6006)
