import socket
import sys
import time
hostname=sys.argv[1]
port=int(sys.argv[2])
protocolPhase="s"
measurementType="rtt"
numProbes="10"
msgSizes=["1","100","200","400","800","1000","1000","2000","4000","8000","16000","32000"]
measurements=[]
serverDelay=0
for i in range(len(msgSizes)):
    mysocket=socket.socket()
    print(mysocket.connect((hostname,port)))
    if i>5:
        measurementType="tput"
    size=msgSizes[i]
    sendstring=protocolPhase+" "+measurementType+" "+numProbes+" "+size+" "+str(serverDelay)+"\n"
    size=int(size)
    measurements.append(size)
    mysocket.sendall(sendstring.encode())
    response=""
    while response=="" or response[-1]!="\n":
        response+=mysocket.recv(1024).decode()
    if(response)!="200 OK: Ready\n":
        exit()
    else:
        for x in range(int(numProbes)):
            sendstring="m"+" "+str(x+1)+" "+"W"*(size)+"\n"
            timesend=time.time()
            mysocket.sendall(sendstring.encode())
            msg=""
            while len(msg)==0 or msg[-1]!="\n":
                msg+=mysocket.recv(size+128).decode()
            timereceive=time.time()
            if(measurementType=="tput"):
                measurements.append(size/((timereceive-timesend)+.0000000000001))
            else:
                measurements.append(timereceive-timesend)
            print(measurements)
    sendstring="t\n"
    mysocket.sendall(sendstring.encode())
    response=""
    while response=="" or response[-1]!="\n":
        print(response)
        response+=mysocket.recv(1024).decode()
    mysocket.close()
