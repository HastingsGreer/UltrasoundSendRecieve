import numpy as np
import socket
import cv2

"""
Dummy Reciever. This code listens on the socket 9999 
and displays the images recieved using openCV.
"""

def process(x, metadata):
    cv2.imshow(metadata, x)
    cv2.waitKey(1)

def get_connection():
    s = socket.socket(socket.AF_INET,
	              socket.SOCK_STREAM)

    s.bind(("", 9999))

    s.listen(1)
    conn, addr = s.accept()
    print("got connection")

    lenMetadata = np.frombuffer(conn.recv(4), dtype=np.int32)[0]

    metadata = str(conn.recv(lenMetadata), "utf-8")

    width, height = np.frombuffer(conn.recv(8), dtype=np.int32)

    print(width, height)
    while True:
        message_list = []
        while sum([len(m) for m in message_list]) < width * height * 2:
            message = conn.recv(width * height * 2)
            if len(message) == 0:
                print("connection died")
                s.close()
                return
            message_list.append(message)
        message = b"".join(message_list)

        x = np.fromstring(message, dtype=np.uint16).reshape((height, width))
        process(x, metadata)

        #conn.send(res.astype(np.float32).tobytes())
    	
while True:
    get_connection()