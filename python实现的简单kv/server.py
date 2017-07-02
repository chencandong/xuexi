# -*- coding:utf-8 -*-
"""定义编码类型"""

import Queue
import sys
import socket
import select
import getopt
import requests

DICT = {}
AUTH_STATUS = {}


class KvData(object):
    """定义操作全局字典类"""
    def __init__(self, addr_id):
        """初始化全局字典类"""
        self.addr_id = addr_id

    def execute(self, command):
        """执行命令操作字典"""
        cmd = command.split()
        print cmd
        if len(cmd) == 3 and cmd[0] == "AUTH":
            result = self.init_passwd(cmd)
        elif len(cmd) == 3 and cmd[0] == "SET":
            result = self.set_kv(cmd[1], cmd[2])
        elif len(cmd) == 2 and  cmd[0] == "GET":
            result = self.get_kv(cmd[1])
        elif len(cmd) == 3 and cmd[0] == "URL":
            result = self.get_httpstat(cmd[1], cmd[2])
        else:
            result = {"errcode": -1, "desc": "wrong command"}
        return result

    def init_passwd(self, command):
        """初始化密码"""
        with open('auth.conf') as f:
            for line in f:
                line = line.strip('\n')
                if line:
                    line = line.split()
                    print "auth", line[0], command[1], line[1], command[2]
                    if line[0] == command[1] and line[1] == command[2]:
                        AUTH_STATUS[self.addr_id] = True
                        print "login successful"
                        print AUTH_STATUS
                        return {"errcode": 0, "desc": "login succssful"}
                    else:
                        AUTH_STATUS[self.addr_id] = False
        return {"errcode": -1, "desc": "no such user or wrong passwd"}

    def set_kv(self, key, value):
        """配置key-value"""
        if self.addr_id in AUTH_STATUS and AUTH_STATUS[self.addr_id]:
            DICT[key] = value
            result = {"errcode": 0, "desc": "sccusful"}
        else:
            result = {"errcode": -1, "desc": "you don't have the permission"}
        return result

    def get_kv(self, key):
        """获取key-value"""
        if self.addr_id in AUTH_STATUS and AUTH_STATUS[self.addr_id]:
            if key in DICT:
                result = {"errcode:": 0, "value": DICT[key]}
            else:
                result = {"errcode": -1, "desc": "no such key "}
        else:
            result = {"errcode": -1, "desc": "you don't have the permission"}
        return  result

    def get_httpstat(self, name, url):
        """获取url的http状态"""
        if self.addr_id in AUTH_STATUS and AUTH_STATUS[self.addr_id]:
            try:
                r = requests.get(url)
                http_code = r.status_code
                if "content-length" in r.headers:
                    content_length = r.headers["content-length"]
                else:
                    content_length = ""

                self.set_kv(name, {"http_code":http_code, "content_length": content_length})
                result = {"errcode": 0, "http_code":http_code, "content_length": content_length}
            except Exception as e:
                result = {"errcode": -1, "desc": e}
        else:
            result = {"errcode": -1, "desc": "you don't have the permission"}
        return result

class KvServer(object):
    """初始化kv服务器"""
    def __init__(self, host_name, port_num, buff_size=1024, time_out=20):
        try:
            self.__host = host_name
            self.__port = port_num
            self.__time_out = time_out
            self.__buffsize = buff_size

            # self.conn,self.addr = self.s.accept()
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setblocking(False)
            self.s.settimeout(self.__time_out)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # SOL_SOCKET套接字描述符，SO_REUSEADDR端口复用
            print "ip %s binding........"%self.__host
            self.s.bind((self.__host, self.__port))
            self.s.listen(10)
            print "port %s  listening ........"%self.__port

        except socket.error as e:
            print "errcode:%s;desc:%s" % (e[0], e[1])
            raise

        self.inputs = [self.s]
        self.outputs = []
        self.message_queues = {}
        self.client_info = {}

    def run(self):
        """运行kv服务器"""
        running = True
        while running:
            rs, ws, es = select.select(self.inputs, self.outputs, self.inputs, 20)
            if not (rs or ws or es):
                continue

            for s in rs:
                if s == self.s:
                    conn, addr = s.accept()
                    print 'connect from %s' % (addr[0]+":"+str(addr[1]))
                    conn.setblocking(0)
                    self.inputs.append(conn)
                    self.client_info[conn] = (addr[0]+":"+str(addr[1]))
                    self.message_queues[conn] = Queue.Queue()
                else:
                    try:
                        data = s.recv(self.__buffsize)
                        if data:
                            print "Receive from %s"%data
                            self.message_queues[s].put(data)
                            if s not in self.outputs:
                                self.outputs.append(s)

                    except socket.error as e:
                        self.inputs.remove(s)
                        del self.message_queues[s]
                        print "disconnect from %s" % str(self.client_info[s])
                        addr_id = self.client_info[s]
                        if addr_id in AUTH_STATUS:
                            del AUTH_STATUS[addr_id]
                        del self.client_info[s]

            for output in self.outputs:
                try:
                    if not self.message_queues[output].empty():
                        command = self.message_queues[output].get()
                        addr = self.client_info[output]
                        kv = KvData(addr)
                        result = kv.execute(command)
                        output.sendall(str(result))

                    else:
                        self.outputs.remove(output)

                except socket.error as e:
                    print e
                    del self.message_queues[output]
                    self.outputs.remove(output)
                    print "disconnection from %s"%self.client_info[output]
                    if addr_id in AUTH_STATUS:
                        del AUTH_STATUS[output]

if __name__ == "__main__":
    host = "127.0.0.1"
    port = "5678"
    opts, args = getopt.getopt(sys.argv[1:], 'h:p:', ["host=", "port="])
    for k, v in opts:
        if k in ('-h', '--host'):
            host = v
        if k in ('-p', '--port'):
            port = v
    ks = KvServer(host, int(port))
    ks.run()