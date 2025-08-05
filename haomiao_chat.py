import ollama
import streamlit as st

#ollama需要获取客户端
client = ollama.Client(host="http://localhost:11434")

#初始化消息记录
if 'message' not in st.session_state:
    st.session_state['message']=[]#第一次执行，需要将session_state进行初始化，使message=一个空的list

#添加标题
st.title("浩淼智聊")

#添加分割线
st.divider()

#用户输入问题
prompt = st.chat_input("请输入你的问题：")

#判断，如果用户输入了内容，则开始工作
if prompt:
    #将用户的问题添加到历史记录中
    st.session_state['message'].append({"role":"user","content":prompt})
    #for循环将历史消息全部输出到消息容器内
    for message in st.session_state['message']:
        st.chat_message(message['role']).markdown(message['content'])

    with st.spinner("思考中……"):
        response = client.chat(
            model="qwen3:0.6b",
            messages = [{"role":"user","content":prompt}]
        )
        #从response中取出message和content两个key
        st.session_state['message'].append({"role":"assistant","content":response['message']['content']})
        #在页面中渲染AI的回答
        st.chat_message("assistant").markdown(response['message']['content'])
