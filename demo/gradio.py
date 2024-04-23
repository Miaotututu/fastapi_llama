import gradio as gr
import requests
import json

block = gr.Blocks()
prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "


def chatgpt_clone(input_question, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input_question)
    data = {"text": prompt,
            "db_name": "dimp",
            "user_question": input_question}
    print(data)
    url = "http://0.0.0.0:6667/getSqlAnswer"
    response = requests.post(url, data=json.dumps(data))
    if response.status_code != 200:
        return "error"
    resp = response.json()
    output = resp['result']
    history.append((input_question, output))
    return history, history


with block:
    gr.Markdown("""<h1><center>DataQueryAI-SQLTune1.0</center></h1>
    """)
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder=prompt)
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])

gr.close_all()  # 关闭所有正在运行的端口
block.launch(debug=True, share=True, server_port=6006)
