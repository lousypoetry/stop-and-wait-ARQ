from socket import *
import os
import time
import random

serverPort=12000
serverSocket=socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('',serverPort))
print 'I am ready to send...'
f=open("shakespeare.txt","rb")
Slast=0
count=1
timeout=0.008
send=0
message, clientAddress=serverSocket.recvfrom(2048)
while True:
        data = f.readline()
        while data:
                #simulate frame loss
                if random.randint(0,9)!=0:
                        serverSocket.sendto(bytes(str(Slast)+data).encode(),clientAddress)
                        print('The '+str(count)+'th frame is sent successfully, Slast='+str(Slast)+': '+str(Slast)+str(data).strip())
                        send+=1
                else:
                        print('The '+str(count)+'th frame is sent but lost, Slast='+str(Slast))
                #wait for ack
                while True:
                        serverSocket.settimeout(timeout)
                        #not exceeding time
                        try:
                                ack, clientAddress=serverSocket.recvfrom(2048)
                                #receive ack
                                tmp=str(ack)
                                if tmp[0:1]==str((Slast+1)%2):
                                        print('I have received ACK='+tmp[0:1]+'\n')
                                        Slast=(Slast+1)%2
                                        count+=1
                                        break
                        #timeout, resend
                        except:
                                print 'Timeout. I did not receive ACK='+str((Slast+1)%2)
                                #simulate frame loss
                                if random.randint(0,9)!=0:
                                        serverSocket.sendto(bytes(str(Slast)+data).encode(),clientAddress)
                                        print('The '+str(count)+'th frame is resent successfully, Slast='+str(Slast)+': '+str(Slast)+str(data).strip())
                                        send+=1
                                else:
                                        print('The '+str(count)+'th frame is resent but lost')

                data=f.readline()

        #finish sending
        serverSocket.sendto('endd'.encode(),clientAddress)
        break

print('Done!'+str(count-1)+' frames are sent successfully. Total number of transmissions: '+str(send))
f.close()
serverSocket.close()

