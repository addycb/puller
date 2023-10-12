import socket 
import sys
#Server program. Binds to socket, listens, echoes message and closes connection when message received 
port=int(sys.argv[1])
mysocket=socket.socket()
mysocket.bind(('',port))
mysocket.listen()
while True:
    conn,address=mysocket.accept()
    msg=conn.recv(4096)
    print(msg.decode())
    conn.send(msg)
    conn.close()
    break


