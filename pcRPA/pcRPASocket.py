import socketio
import eventlet
from win32api import SetConsoleCtrlHandler

# 启动服务器
import getopt
import sys
class ChatServer:
    def __init__(self):
        # 创建Socket.IO服务器实例
        self.sio = socketio.Server(cors_allowed_origins='*')
        self.app = socketio.WSGIApp(self.sio)

        # 注册事件处理
        self.sio.on('connect', self.handle_connect)
        self.sio.on('disconnect', self.handle_disconnect)
        self.sio.on('rpa_tool_message', self.handle_message)

    def handle_connect(self, sid, environ):
        print(f"用户 {sid} 已连接")
        self.sio.emit('rpa_tool_message', {'user': '系统', 'message': f'用户 {sid} 连接成功'}, room=sid)

    def handle_disconnect(self, sid):
        print(f"用户 {sid} 已断开连接")
        self.sio.emit('rpa_tool_message', {'user': '系统', 'message': f'用户 {sid} 断开连接'})

    def handle_message(self, sid, data):
        print(f"用户 {sid} 发送消息: {data['message']}")
        if data["message"] == "exit" :
            exit()
        # 广播消息给所有用户
        self.sio.emit('rpa_tool_message', {'message': data['message']})

    def run(self, host='0.0.0.0', port=5000):
        eventlet.wsgi.server(eventlet.listen((host, port)), self.app)

def main(port=5000):
    server = ChatServer()
    server.run(port=port)

def handler(event):
    if event == 0:
        exit()

if __name__ == '__main__':
   
    print("start")
    SetConsoleCtrlHandler(handler, 1)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:s:p:", ["file=", "source=", "port="])
    except getopt.GetoptError as err:
        print(err)  
        sys.exit(2)
    for o, a in opts:
        if o in ("-p", "--port"):
            main(port=int(a))
