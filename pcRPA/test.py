import socketio

sio = socketio.Client()

def socketioInit(port=5000):
    # 连接服务端 IP+端口
    sio.connect('http://localhost:'+str(port))

def socketioSend(ut):
    # 向服务端发送消息
    sio.emit('rpa_tool_message', ut)

