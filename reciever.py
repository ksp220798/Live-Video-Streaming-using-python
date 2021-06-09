import socket
import cv2,pickle,struct

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #TCP connection
print("ENter your IP")
ip=input()
print("ENter your PORT")
port=int(input())
s.bind((ip,port))
print("ENter your streamer's IP")
ip1=input()
print("ENter streamer's PORT")
port1=int(input())
s.connect((ip1,port1))
cap=cv2.VideoCapture(0)
data = b""
payload_size = struct.calcsize("Q")   #8 bytes
while True:
    while len(data) < payload_size:
        packet = s.recv(4*1024) #4k buffersize
        if not packet: break    #if no data, then break
        data+=packet            #if data comes,append to data until buffer full
    packed_msg_size = data[:payload_size]   #first 8 bytes have packed msg
    data = data[payload_size:]   #after initial 8 bytes, frame data present
    msg_size = struct.unpack("Q",packed_msg_size)[0] #unpacking packed message and getting 
    
    while len(data) < msg_size:            
        data += s.recv(4*1024)
    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("RECEIVING VIDEO",frame)
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q'):
        break
s.close()
