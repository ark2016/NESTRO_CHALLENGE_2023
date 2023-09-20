from socket import *
import sys

host = '127.0.0.1'
port = 8081
addr = (host,port)


tcp_socket = socket(AF_INET, SOCK_STREAM)
tcp_socket.connect(addr)
while(True):
    data = input('write to server: ')
    if data=='break':
        break
    data+="\n"
    if not data :
        tcp_socket.close()
        sys.exit(1)

    #encode - перекодирует введенные данные в байты, decode - обратно
    data = str.encode(data)
    tcp_socket.send(data)
    data = bytes.decode(data)
    data = tcp_socket.recv(1024)
    print(data)

tcp_socket.close()
