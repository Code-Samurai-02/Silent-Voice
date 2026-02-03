import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening for multiple ESP32s...")

while True:
    data, addr = sock.recvfrom(1024)
    sender_ip = addr[0] # This extracts the IP (e.g., 192.168.1.50)
    message = data.decode()
    
    print(f"[{sender_ip}] says: {message}")