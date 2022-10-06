import socket
import keyboard


def forward():
    UDPClientSocket.sendto(str.encode("forward"), serverAddressPort)
    print("forward sent")


def back():
    UDPClientSocket.sendto(str.encode("back"), serverAddressPort)
    print("back sent")


def left():
    UDPClientSocket.sendto(str.encode("left"), serverAddressPort)
    print("left sent")


def right():
    UDPClientSocket.sendto(str.encode("right"), serverAddressPort)
    print("right sent")


def turnRight():
    UDPClientSocket.sendto(str.encode("turnRight"), serverAddressPort)
    print("turnRight sent")


def turnLeft():
    UDPClientSocket.sendto(str.encode("turnLeft"), serverAddressPort)
    print("turnLeft sent")


def up():
    UDPClientSocket.sendto(str.encode("up"), serverAddressPort)
    print("up sent")


def down():
    UDPClientSocket.sendto(str.encode("down"), serverAddressPort)
    print("down sent")


if __name__ == '__main__':
    msgFromClient = "Hello UDP Server"
    bytesToSend = str.encode(msgFromClient)
    serverAddressPort = ("192.168.1.246", 20001)
    bufferSize = 1024

    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    # msgFromServer = UDPClientSocket.recvfrom(bufferSize)  # Receiving that the connection was successful and the client is permitted to start sending commands to drone
    # msg = "Message from Server: {}".format(msgFromServer[0])
    # print(msg)

    keyboard.add_hotkey('w', forward, timeout=0)
    keyboard.add_hotkey('s', back, timeout=0)
    keyboard.add_hotkey('a', left, timeout=0)
    keyboard.add_hotkey('d', right, timeout=0)
    keyboard.add_hotkey('e', turnRight, timeout=0)
    keyboard.add_hotkey('q', turnLeft, timeout=0)
    keyboard.add_hotkey('page up', up, timeout=0)
    keyboard.add_hotkey('page down', down, timeout=0)

    keyboard.wait()  # infinite wait
