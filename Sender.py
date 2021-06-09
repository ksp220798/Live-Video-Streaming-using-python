import socket,pickle,struct
import cv2
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #TCP connection

print("Enter Your IP")
ip=input()
print("Enter Your port")
port=int(input())
print("Enter Your Partner IP")
pip=input()
print("Enter Your Partner port")
pport=int(input())

s.bind((ip,port))
s.listen(5)  #5 is backlog meaning it can accept 5 connections at a time
cap = cv2.VideoCapture(0)
while True:
    client_socket,addr = s.accept()
    print('GOT CONNECTION FROM:',addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        
        while(vid.isOpened()):
            img,frame = vid.read()
            a = pickle.dumps(frame)   #serialize frame to byte data
            message = struct.pack("Q",len(a))+a #pack each frame #Q is 8 bytes
            client_socket.sendall(message)
            
            cv2.imshow('TRANSMITTING VIDEO',frame)
            key = cv2.waitKey(1) & 0xFF
            if key ==ord('q'):     #press q to exit
                client_socket.close()
