import cv2
import socket
import struct
import pickle
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 8485))
connection = client_socket.makefile('wb')
cam = cv2.VideoCapture(0)
# cam.set(3, 320)
# cam.set(4, 240)
img_counter = 0
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
def rece():
    global img_counter
    while True:
        ret, frame = cam.read()
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(frame, 0)
        size = len(data)
        print("{}: {}".format(img_counter, size))
        client_socket.sendall(struct.pack(">L", size) + data)
        img_counter += 1
        if img_counter % 30 == 0:
            msg = client_socket.recv(1024)
            if msg:
                # 接收服务端返回的数据，需要解码
                print(msg.decode("utf-8"))
        timer2 = threading.Timer(0.02, rece)
        timer2.start()
    cam.release()

rece()
