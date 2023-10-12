import socket
import sys
hostname=sys.argv[1]
port=int(sys.argv[2])
mysocket=socket.socket()
mysocket.connect((hostname,port))
mysocket.send("this my string".encode())
print(mysocket.recv(4096).decode())
mysocket.close()
