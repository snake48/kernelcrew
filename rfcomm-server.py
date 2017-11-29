# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *
from time import sleep
import threading
from Adafruit_MotorHAT import Adafruit_MotorHAT,Adafruit_StepperMotor
import atexit
mh=Adafruit_MotorHAT(addr=0x60)
my=mh.getStepper(200,1)
my.setSpeed(1000)
my2=mh.getStepper(200,2)
my2.setSpeed(1000)
def t1():
    my.step(100,Adafruit_MotorHAT.FORWARD,Adafruit_MotorHAT.DOUBLE)

def t2():
    my2.step(100,Adafruit_MotorHAT.FORWARD,Adafruit_MotorHAT.DOUBLE)
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        print("received [%s]" % data)
        print(data)
        #if str(data)=="b'motor'":
        if len(data)==10:
            print('yes')
            threads=[]
            t=threading.Thread(target=t1)
            tt=threading.Thread(target=t2)
            threads.append(t)
            threads.append(tt)
            t.start()
            tt.start()
            
except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")
