import socket
import cv2
import pickle
import struct

HOST='127.0.0.1'
PORT=8485
socketserver=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

socketserver.bind((HOST,PORT))
print('Socket bind complete')
socketserver.listen(10)
print('Socket now listening')

clientsocket,addr=socketserver.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += clientsocket.recv(4096)

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += clientsocket.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow('ImageWindow',frame)
    cv2.waitKey(1)
    msg = "GoGoGo"
    # 对要发送的数据进行编码
    clientsocket.send(msg.encode("utf-8"))