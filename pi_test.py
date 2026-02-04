import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening for multiple ESP32s...")

present_char = ""
temp = ""

while True:
    data, addr = sock.recvfrom(1024)
    sender_ip = addr[0] # This extracts the IP (e.g., 192.168.1.50)
    message = data.decode()
    thumb_finger = ""
    index_finger = ""
    middle_finger = ""
    ring_finger = ""
    pinky_finger = ""
    
    if sender_ip == "192.168.1.21":
        thumb_finger = message
    elif sender_ip == "192.168.1.17":
        index_finger = message
    elif sender_ip == "192.168.1.18":
        middle_finger = message
    elif sender_ip == "192.168.1.20":
        ring_finger = message
    elif sender_ip == "192.168.1.19":
        pinky_finger = message
    
    if thumb_finger == "Thumb Error" or index_finger == "Index Error" or middle_finger == "Middle Error" or ring_finger == "Ring Error" or pinky_finger == "Pinky Error":
        continue
    elif thumb_finger == "Thumb Up" and index_finger == "Index Up" and middle_finger == "Middle Up" and ring_finger == "Ring Up" and pinky_finger == "Pinky Up":
        present_char = ""
        continue
    elif thumb_finger == "Thumb Up" and index_finger == "Index Down" and middle_finger == "Middle Down" and ring_finger == "Ring Down" and pinky_finger == "Pinky Down":
        if present_char == "A":
            continue
        else:
            present_char = "A"
            temp += "A"
    elif thumb_finger == "Thumb Half" and index_finger == "Index Up" and middle_finger == "Middle Up" and ring_finger == "Ring Up" and pinky_finger == "Pinky Up":
        if present_char == "B":
            continue
        else:
            present_char = "B"
            temp += "B"
    elif thumb_finger == "Thumb Half" and index_finger == "Index Half" and middle_finger == "Middle Half" and ring_finger == "Ring Half" and pinky_finger == "Pinky Half":
        if present_char == "C":
            continue
        else:
            present_char = "C"
            temp += "C"
    elif thumb_finger == "Thumb Half" and index_finger == "Index Up" and middle_finger == "Middle Half" and ring_finger == "Ring Half" and pinky_finger == "Pinky Half":
        if present_char == "D":
            continue
        else:
            present_char = "D"
            temp += "D"
    elif thumb_finger == "Thumb Down" and index_finger == "Index Half" and middle_finger == "Middle Half" and ring_finger == "Ring Half" and pinky_finger == "Pinky Half":
        if present_char == "E":
            continue
        else:
            present_char = "E"
            temp += "E"
    elif thumb_finger == "Thumb Half" and index_finger == "Index Half" and middle_finger == "Middle Up" and ring_finger == "Ring Up" and pinky_finger == "Pinky Up":
        if present_char == "F":
            continue
        else:
            present_char = "F"
            temp += "F"
    elif thumb_finger == "Thumb Half" and index_finger == "Index Half" and middle_finger == "Middle Down" and ring_finger == "Ring Down" and pinky_finger == "Pinky Down":
        if present_char == "G":
            continue
        else:
            present_char = "G"
            temp += "G"
    elif thumb_finger == "Thumb Half" and index_finger == "Index Half" and middle_finger == "Middle Half" and ring_finger == "Ring Down" and pinky_finger == "Pinky Down":
        if present_char == "H":
            continue
        else:
            present_char = "H"
            temp += "H"
    elif thumb_finger == "Thumb Up" and index_finger == "Index Down" and middle_finger == "Middle Down" and ring_finger == "Ring Down" and pinky_finger == "Pinky Up":
        if present_char == "I":
            continue
        else:
            present_char = "I"
            temp += "I"
    elif thumb_finger == "Thumb Up" and index_finger == "Index Down" and middle_finger == "Middle Down" and ring_finger == "Ring Up" and pinky_finger == "Pinky Up":
        if present_char == "J":
            continue
        else:
            present_char = "J"
            temp += "J"
    elif thumb_finger == "Thumb Up" and index_finger == "Index Up" and middle_finger == "Middle up" and ring_finger == "Ring Down" and pinky_finger == "Pinky Down":
        if present_char == "K":
            continue
        else:
            present_char = "K"
            temp += "K"
    elif thumb_finger == "Thumb Half" and index_finger == "Index Up" and middle_finger == "Middle Down" and ring_finger == "Ring Down" and pinky_finger == "Pinky Down":
        if present_char == "L":
            continue
        else:
            present_char = "L"
            temp += "L"
    elif thumb_finger == "Thumb Half" and index_finger == "Index Down" and middle_finger == "Middle Down" and ring_finger == "Ring Down" and pinky_finger == "Pinky Down":
        if present_char == "M":
            continue
        else:
            present_char = "M"
            temp += "M"
    elif thumb_finger == "Thumb Half" and index_finger == "Index Half" and middle_finger == "Middle Half" and ring_finger == "Ring Down" and pinky_finger == "Pinky Down":
        if present_char == "N":
            continue
        else:
            present_char = "N"
            temp += "N"
    elif thumb_finger == "Thumb Down" and index_finger == "Index Down" and middle_finger == "Middle Down" and ring_finger == "Ring Down" and pinky_finger == "Pinky Down":
        if present_char == "O":
            continue
        else:
            present_char = "O"
            temp += "O"
    elif thumb_finger == "Thumb Half" and index_finger == "Index Down" and middle_finger == "Middle Half" and ring_finger == "Ring Half" and pinky_finger == "Pinky Down":
        if present_char == "P":
            continue
        else:
            present_char = "P"
            temp += "P"
    elif thumb_finger == "Thumb Down" and index_finger == "Index Half" and middle_finger == "Middle Down" and ring_finger == "Ring Down" and pinky_finger == "Pinky Down":
        if present_char == "Q":
            continue
        else:
            present_char = "Q"
            temp += "Q"
    elif thumb_finger == "Thumb Half" and index_finger == "Index Up" and middle_finger == "Middle Up" and ring_finger == "Ring Down" and pinky_finger == "Pinky Down":
        if present_char == "R":
            continue
        else:
            present_char = "R"
            temp += "R"
    elif thumb_finger == "Thumb Down" and index_finger == "Index Half" and middle_finger == "Middle Half" and ring_finger == "Ring Down" and pinky_finger == "Pinky Down":
        if present_char == "S":
            continue
        else:
            present_char = "S"
            temp += "S"
    elif thumb_finger == "Thumb Up" and index_finger == "Index Half" and middle_finger == "Middle Down" and ring_finger == "Ring Down" and pinky_finger == "Pinky Down":
        if present_char == "T":
            continue
        else:
            present_char = "T"
            temp += "T"
    elif thumb_finger == "Thumb Down" and index_finger == "Index Up" and middle_finger == "Middle Up" and ring_finger == "Ring Down" and pinky_finger == "Pinky Down":
        if present_char == "U":
            continue
        else:
            present_char = "U"
            temp += "U"
    elif thumb_finger == "Thumb Up" and index_finger == "Index Up" and middle_finger == "Middle Up" and ring_finger == "Ring Down" and pinky_finger == "Pinky Down":
        if present_char == "V":
            continue
        else:
            present_char = "V"
            temp += "V"
    elif thumb_finger == "Thumb Down" and index_finger == "Index Up" and middle_finger == "Middle Up" and ring_finger == "Ring Up" and pinky_finger == "Pinky Down":
        if present_char == "W":
            continue
        else:
            present_char = "W"
            temp += "W"
    elif thumb_finger == "Thumb Down" and index_finger == "Index Up" and middle_finger == "Middle Down" and ring_finger == "Ring Down" and pinky_finger == "Pinky Down":
        if present_char == "X":
            continue
        else:
            present_char = "X"
            temp += "X"
    elif thumb_finger == "Thumb Up" and index_finger == "Index Up" and middle_finger == "Middle Down" and ring_finger == "Ring Down" and pinky_finger == "Pinky Up":
        if present_char == "Y":
            continue
        else:
            present_char = "Y"
            temp += "Y"
    elif thumb_finger == "Thumb Down" and index_finger == "Index Down" and middle_finger == "Middle Down" and ring_finger == "Ring Down" and pinky_finger == "Pinky Up":
        if present_char == "Z":
            continue
        else:
            present_char = "Z"
            temp += "Z"
    print(f"[{sender_ip}] says: {message}")