import socket

class Server(object):
    def __init__(self,clients,port):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind(('127.0.0.1',port))
        self.s.listen(clients)

    def acceptClients(self):
        self.conn = self.s.accept()[0]

    def write(self,message):
        self.conn.send(message + '\n')

    def read(self):
        a = ' '
        b = ''
        while a != '\n':
            a = self.conn.recv(1)
            b = b + a
        return b

    def close(self):
        self.conn.close()
