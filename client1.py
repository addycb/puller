import socket
import sys
import time
hostname=sys.argv[1]
port=int(sys.argv[2])
mysocket=socket.socket()

mysocket.connect((hostname,port))
protocolPhase="s"
measurementType="rtt"
numProbes="10"
msgSizes=["1","100","200","400","800","1000","1000","2000","4000","8000","16000","32000"]
measurements=[]
serverDelay=0
for i in range(len(msgSizes)):
    if i>5:
        measurementType="tput"
    size=msgSizes[i]
    sendstring=protocolPhase+" "+measurementType+" "+numProbes+" "+size+" "+str(serverDelay)+"\n"
    size=int(size)
    measurements.append(size)
    #print(sendstring)
    mysocket.sendall(sendstring.encode())
    if(mysocket.recv(1024).decode())!="200 OK: Ready":
        exit()
    else:
        for x in range(int(numProbes)):
            sendstring="m"+" "+str(x+1)+" "+"W"*(size)+"\n"
            timesend=time.time()
            #print(sendstring)
            mysocket.sendall(sendstring.encode())
            msg=""
            while len(msg)==0 or msg[-1]!="\n":
                msg+=mysocket.recv(size+128).decode()
            #print("msg get: "+msg)
            #print(len(msg))
            timereceive=time.time()
            if(measurementType=="tput"):
                measurements.append(size/(timereceive-timesend))
            else:
                measurements.append(timereceive-timesend)
            print(measurements)
sendstring="t\n"
#print(sendstring)
mysocket.sendall(sendstring.encode())
print(mysocket.recv(1024).decode())    
mysocket.close()
