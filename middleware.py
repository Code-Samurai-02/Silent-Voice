import socket

HOST = "127.0.0.1"
PORT = 5000

def send_text(text):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.send(text.encode())
    client.close()

if __name__ == "__main__":
    while True:
        text = input("Enter text (exit to quit): ")
        if text == "exit":
            break
        send_text(text)