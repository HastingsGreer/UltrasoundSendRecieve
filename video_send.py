import socket
import numpy as np
import time
import argparse
import imageio

"""
Video sender. Takes the name of an ultrasound video as an argument, and sends
that video over the network, pretending that it is taken in real time
"""

parser = argparse.ArgumentParser(description='Send a video')
parser.add_argument('filename', help="file to send")
args = parser.parse_args()

host = socket.gethostname()    
port = 9999             # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))


metadata = '{"probe":"video_file", "filename":"' + args.filename + '""}'

reader = imageio.get_reader(args.filename, 'ffmpeg')
image = reader.get_next_data()[:, :, 0]

s.sendall(np.array([len(metadata)], dtype=np.int32).tobytes())
s.sendall(bytes(metadata, "utf-8"))

width = image.shape[1]
height = image.shape[0]
s.sendall(np.array([width, height], dtype=np.int32).tobytes())

while True:
	s.sendall(image.astype(np.uint16).tobytes())
	image = reader.get_next_data()[:, :, 0]
	time.sleep(.05)

