
from socket import *

defhost = '127.0.0.1'
defport = 21563

HOST = raw_input("input host:")
if not HOST:
    HOST = defhost
    print "nothing input set to default!"
PORT = (raw_input("input port:"))
if not PORT:
    PORT = defport
    print "nothing input set to default!"

PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    
    data = raw_input('> ')
    if not data:
        break
    tcpCliSock.send(data)
    data = tcpCliSock.recv(BUFSIZ)
    if not data:
        break
    print str(data)


tcpCliSock.close()
