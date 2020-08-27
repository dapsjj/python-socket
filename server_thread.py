import socket
import cv2
import pickle
import struct
from datetime import datetime
import threading

HOST='127.0.0.1'
PORT=8485
socketserver=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

socketserver.bind((HOST,PORT))
print('Socket bind complete')
socketserver.listen(10)
print('Socket now listening')
counter = 1

def receive_timer():
    clientsocket, addr = socketserver.accept()
    global counter
    data = b""
    payload_size = struct.calcsize(">L")
    # print("payload_size: {}".format(payload_size))
    while True:
        counter += 1
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
        if counter % 10 == 0:  # add condition
            msg = "Go"
            clientsocket.send(msg.encode("utf-8"))
        timer2 = threading.Timer(0.02, receive_timer)
        timer2.start()

receive_timer()
