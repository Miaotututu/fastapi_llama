import gradio as gr
#该函数有3个输入参数和2个输出参数
def greet(name, picacg, temperature):
    salutation = "Good morning" if picacg else "Good evening"
    greeting = f"{salutation} {name}. It is {temperature} degrees today"
    celsius = (temperature - 32) * 5 / 9
    return greeting, round(celsius, 2)


demo = gr.Interface(
    fn=greet,
    #按照处理程序设置输入组件
    inputs=["text", "checkbox", gr.Slider(0, 100)],
    #按照处理程序设置输出组件
    outputs=["text", "number"],
)
demo.launch()