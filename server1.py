import socket 
import sys
import time
#This program is a pretty straightforward echo server, that receives 3 types of messages: those with payloads to be echoed, those foretelling coming message tests and their properties,
# and a termination message. We use a class to abstract the settings receieved  from the "foretelling" messages, and loops to ensure that packets receieved in a stream are pieced together 
#  correctly, as we only stop when we see a termination character '\n'. Our server also expects a new connection for every message test set. We also print status codes to the command line. 

class Settings:
    def __init__(self,varList=[None,None,0,0,0]):
        self.protocolPhase=varList[0]
        self.measurementType=varList[1]
        self.numberofProbes=int(varList[2])
        self.thisProbe=1
        self.msgSize=int(varList[3]) 
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
    match msg[0]:
        case "s":
            currSettings=Settings(msg[:-1].split(" "))
            conn.sendall("200 OK: Ready\n".encode())          
        case "m":
            probenum=int((msg.split(" "))[1])
            if (probenum!=currSettings.thisProbe) or (probenum>(currSettings.numberofProbes)) :
                conn.sendall("404 ERROR: Invalid Measurement Message\n".encode())
                conn.close()
                conn,address=mysocket.accept()
            else:
                time.sleep(currSettings.serverDelay)
                conn.sendall(msg.encode())
                currSettings.thisProbe+=1
        case "t":
                if(len(msg)>2):
                    conn.sendall("404 ERROR: Invalid Connection Termination Message\n".encode())
                else:
                    conn.sendall("200 OK: Closing Connection\n".encode())
                conn.close()
                conn,address=mysocket.accept()

            
    
    

