import ollama


def analyse_response(ask_message):
    response = ollama.chat(model='qwen:7B', messages=[
        {
            'role': 'user',
            'content': ask_message,
        },
    ])
    return response['message']['content']


# 函数调用方法如下：
# question = '为什么白色比黑色白？'
# answer = analyse_response(question)
# print(answer)
