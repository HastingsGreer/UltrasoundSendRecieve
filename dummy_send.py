import socket
import numpy as np
import time

"""
Dummy sender. This program takes the place of the probe specific code.
This code sends expanding circles, as a test. Real code will connect
to an ultrasound probe and send ultrasound images
"""

host = socket.gethostname()    
port = 9999             # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))


metadata = '{"probe":"fake_circle", "mm_per_pixel":".8"}'

s.sendall(np.array([len(metadata)], dtype=np.int32).tobytes())
s.sendall(bytes(metadata, "utf-8"))

width = 200
height = 300
s.sendall(np.array([width, height], dtype=np.int32).tobytes())

x, y = np.mgrid[-1:1:300j, -1:1:200j]

r = np.sqrt(x**2 + y**2)
print(r.shape)

while(True):
	for size in np.linspace(0, 1, 100):

		s.sendall(((r < size) * 2**15).astype(np.uint16).tobytes())
		time.sleep(.1)

