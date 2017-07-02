# -*- coding:utf-8 -*-
"""定义编码类型"""
import socket
import getopt
import sys

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 5678
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h:p:', ["host=", "port="])
        for k, v in opts:
            if k in ('-h', '--host'):
                HOST = v
                print HOST
            if k in ('-p', '--port'):
                PORT = int(v)
    except getopt.GetoptError as e:
        print "Error:%s" % e

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    while 1:
        try:
            cmd = raw_input(">>>\n")
            s.sendall(cmd)
            data = s.recv(1024)
            print data
        except socket.error as e:
            print e
    s.close()