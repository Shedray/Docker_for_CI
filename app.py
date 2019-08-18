import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import os
from myDocker.myDocker import ClientHandler,DockerStreamThread
class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        # 向响应中，添加数据
        return self.render('index.html')

class WebsshHanlder(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        dockerCli = ClientHandler(base_url="tcp://139.9.199.194:2375", timeout=1000)
        terminalExecId = dockerCli.creatTerminalExec('f68eb174af36')
        print(terminalExecId)
        self.terminalStream = dockerCli.startTerminalExec(terminalExecId)._sock
        print(self.ws_connection)
        self.terminalThread = DockerStreamThread(self.ws_connection, self.terminalStream)
        self.terminalThread.start()


    def on_message(self, message):
        # print(self.ws_connection)
        print(message)
        self.terminalStream.send(bytes(message, encoding='utf-8'))

    def on_close(self):
        print(self.ws_connection)
        print('ws 已断开')
        print()
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/index', IndexPageHandler),
            (r'/ws', WebsshHanlder)
        ]

        settings = {
            'template_path': 'static',
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()