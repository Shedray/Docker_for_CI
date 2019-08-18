#!/usr/bin/env python
# coding: utf-8

import docker
import threading
import asyncio

class ClientHandler(object):

    def __init__(self, **kwargs):
        self.dockerClient = docker.APIClient(**kwargs)

    def creatTerminalExec(self, containerId):
        execCommand = [
            "/bin/sh",
            "-c",
            'TERM=xterm-256color; export TERM; [ -x /bin/bash ] && ([ -x /usr/bin/script ] && /usr/bin/script -q -c "/bin/bash" /dev/null || exec /bin/bash) || exec /bin/sh']
        execOptions = {
            "tty": True,
            "stdin": True
        }
        execId = self.dockerClient.exec_create(containerId, execCommand, **execOptions)
        return execId["Id"]

    def startTerminalExec(self, execId):
        return self.dockerClient.exec_start(execId, socket=True, tty=True)


class DockerStreamThread(threading.Thread):
    def __init__(self, ws, terminalStream):
        super(DockerStreamThread, self).__init__()
        self.ws = ws
        self.terminalStream = terminalStream

    def run(self):
        print('进程开始')
        asyncio.set_event_loop(asyncio.new_event_loop())
        while self.ws:
            try:
                # print('1')
                dockerStreamStdout = self.terminalStream.recv(2048)
                if dockerStreamStdout is not None:
                    # print(self.ws.stream)
                    # print(dockerStreamStdout)
                    self.ws.write_message(dockerStreamStdout)
                else:
                    print("docker daemon socket is close")
                    self.ws.close
            except Exception as e:
                            print("docker daemon socket err: %s" % e)
                            self.ws.close
                            break
            finally:
                pass