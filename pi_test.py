import socket

# Listen on all interfaces at port 5000
UDP_IP = "0.0.0.0"
UDP_PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

print(f"Pi is ready and listening on port {UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(1024) # Buffer size is 1024 bytes
    print(f"Received message: {data.decode()} from {addr}")