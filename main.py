import socket
import sys
import os

from logic import *

def server():
    print('server', os.getpid())
    
    sock = socket.socket()
    sock.bind(('localhost', 9999))
    sock.listen(1)
    while True:
        conn, addr = sock.accept()

        data = conn.recv(65535)
        if data == None:
            continue

        print(addr, sep='<=>')

        conn.send(server_logic(data))
        conn.close()


def client():
    sock = socket.socket()
    sock.connect(('localhost', 9999))
    
    bdata_to_send = client_logic_data_to_send()
    
    sock.send(bdata_to_send)

    bdata = sock.recv(1024)
    sock.close()

    client_logic_retrive_data(bdata)


if __name__ == '__main__':
    if sys.argv[1] == 'server':
        server()
    if sys.argv[1] == 'client':
        client()