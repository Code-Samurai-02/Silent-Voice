import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5000))

print("UDP server listening...")

while True:
    data, addr = sock.recvfrom(1024)
    temp = ""
    message = data.decode()

    print("Received:", message)
    if(message == "Thumb_Up-Index_Down-Middle_Down-Ring_Down-Pinky_Down"):
        print("A")
    elif(message == "Thumb_Half-Index_Up-Middle_Up-Ring_Up-Pinky_Up"):
        print("B")
    elif(message == "Thumb_Up-Index_Half-Middle_Half-Ring_Half-Pinky_Half"):
        print("C")
    elif(message == "Thumb_Half-Index_Up-Middle_Down-Ring_Down-Pinky_Down"):
        print("D")
    elif(message == "Thumb_Half-Index_Half-Middle_Half-Ring_Half-Pinky_Half"):
        print("E")
    elif(message == "Thumb_Half-Index_Half-Middle_Up-Ring_Up-Pinky_Up"):
        print("F")
    elif(message == "Thumb_Up-Index_Down-Middle_Down-Ring_Half-Pinky_Up"):
        print("G")
    elif(message == "Thumb_Down-Index_Half-Middle_Half-Ring_Down-Pinky_Down"):
        print("H")
    elif(message == "Thumb_Up-Index_Down-Middle_Down-Ring_Down-Pinky_Up"):
        print("I")
    elif(message == "Thumb_Up-Index_Down-Middle_Half-Ring_Half-Pinky_Up"):
        print("J")
    elif(message == "Thumb_Up-Index_Up-Middle_Up-Ring_Down-Pinky_Down"):
        print("K")
    elif(message == "Thumb_Up-Index_Up-Middle_Down-Ring_Down-Pinky_Down"):
        print("L")
    elif(message == "Thumb_Half-Index_Up-Middle_Up-Ring_Down-Pinky_Up"):
        print("M")
    elif(message == "Thumb_Half-Index_Up-Middle_Down-Ring_Half-Pinky_Up"):
        print("N")
    elif(message == "Thumb_Down-Index_Down-Middle_Down-Ring_Down-Pinky_Up"):
        print("O")
    elif(message == "Thumb_Up-Index_Up-Middle_Down-Ring_Half-Pinky_Up"):
        print("P")
    elif(message == "Thumb_Half-Index_Down-Middle_Down-Ring_Half-Pinky_Up"):
        print("Q")
    elif(message == "Thumb_Down-Index_Up-Middle_Up-Ring_Down-Pinky_Down"):
        print("R")
    elif(message == "Thumb_Half-Index_Half-Middle_Half-Ring_Down-Pinky_Down"):
        print("S")
    elif(message == "Thumb_Up-Index_Half-Middle_Down-Ring_Down-Pinky_Down"):
        print("T")
    elif(message == "Thumb_Half-Index_Up-Middle_Up-Ring_Down-Pinky_Down"):
        print("U")
    elif(message == "Thumb_Up-Index_Down-Middle_Up-Ring_Down-Pinky_Up"):
        print("V")
    elif(message == "Thumb_Half-Index_Up-Middle_Up-Ring_Up-Pinky_Down"):
        print("W")
    elif(message == "Thumb_Half-Index_Half-Middle_Down-Ring_Down-Pinky_Down"):
        print("X")
    elif(message == "Thumb_Up-Index_Up-Middle_Down-Ring_Down-Pinky_Up"):
        print("Y")
    elif(message == "Thumb_Up-Index_Up-Middle_Up-Ring_Down-Pinky_Up"):
        print("Z")
    elif(message == "space"):
        print(" ")
    elif(message == "next"):
        print("next")
    elif(message == "."):
        print(".")
    else:
        print("Error")