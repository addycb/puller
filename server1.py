import socket 
import sys
import time

class Settings:
    """
    def __init__(self):
        self.protocolPhase=None
        self.measurementType=None
        self.numberofProbes=None
        self.thisProbe=0
        self.msgSize=1024 #default value for initial msg
        self.serverDelay=0
    """
    def __init__(self,varList=[None,None,0,0,0]):
        self.protocolPhase=varList[0]
        self.measurementType=varList[1]
        self.numberofProbes=int(varList[2])
        self.thisProbe=1
        self.msgSize=int(varList[3]) #default value for initial msg
        self.serverDelay=int(varList[4])

port=int(sys.argv[1])
mysocket=socket.socket()
mysocket.bind(('',port))
mysocket.listen()
conn,address=mysocket.accept()
currSettings=Settings()
while True:
    msg=""
    while len(msg)==0 or msg[-1]!="\n":
        msg+=conn.recv(currSettings.msgSize+128).decode()
    #msg=conn.recv(currSettings.msgSize+128).decode()
    #print("msg get: "+msg)
    #print(len(msg))
    """
    if(currSettings.msgSize>len(msg) and currSettings.thisProbe!=currSettings.numberofProbes+1):
       print(currSettings.msgSize)
       print(len(msg))
       print("fail")
       exit()
    """
    match msg[0]:
        case "s":
            currSettings=Settings(msg[:-1].split(" "))
            conn.sendall("200 OK: Ready".encode())          
        case "m":
            probenum=int((msg.split(" "))[1])
            if (probenum!=currSettings.thisProbe) or (probenum>(currSettings.numberofProbes)+10**-20) :
                conn.sendall("404 ERROR: Invalid Measurement Message".encode())
                conn.close()
                exit()
            else:
                time.sleep(currSettings.serverDelay)
                conn.sendall(msg.encode())
                currSettings.thisProbe+=1
        case "t":
                if(len(msg)>2):
                    conn.sendall("404 ERROR: Invalid Connection Termination Message")
                else:
                    conn.sendall("200 OK: Closing Connection".encode())
                conn.close()
                exit()
    
    

