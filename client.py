from socket import *
import random

serverName='10.3.74.2'
serverPort=12000
clientSocket = socket(AF_INET,SOCK_DGRAM)
message='Hello server.'
clientSocket.sendto(message.encode(),(serverName,serverPort))
Rnext=0
count=1
print('I am ready to receive shakespeare...')
while True:
        if count==1:
                f=open('received_shakespeare.txt','wb')

        data, serverAddress=clientSocket.recvfrom(2048)
        if str(data)!='endd':
                #receive the frame
                tmp=str(data)
                #frame is with correct sequence number
                if (tmp[0:1]==str(Rnext)):
                        f.write(tmp[1:])
                        print('\nI have received the '+str(count)+'th frame: '+str(data).strip())
                        Rnext=(Rnext+1)%2
                        count+=1
                        #simulate ACK loss
                        if random.randint(0,9)!=0:
                                print(('ACK='+str(Rnext)+' is sent successfully'))
                                clientSocket.sendto((str(Rnext)+'ack').encode('utf-8'),(serverName,serverPort))
                        else:
                                print(('ACK='+str(Rnext)+' is sent but lost'))
                #frame is with wrong sequence number
                else:
                        print('I want frame with sequence number='+str(Rnext)+', but I received frame with sequence number='+str(tmp[0:1]))
                        #simulate ACK loss
                        if random.randint(0,9)!=0:
                                print(('ACK='+str(Rnext)+' is sent successfully'))
                                clientSocket.sendto((str(Rnext)+'ack').encode('utf-8'),(serverName,serverPort))
                        else:
                                print(('ACK='+str(Rnext)+' is sent but lost'))

        else:
                break
f.seek(-1, 2)
f.truncate()
print('Done!')
f.close()
clientSocket.close()
