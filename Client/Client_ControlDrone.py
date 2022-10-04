import socket

if __name__ == '__main__':
    msgFromClient = "Hello UDP Server"
    bytesToSend = str.encode(msgFromClient)
    serverAddressPort = ("192.168.1.246", 20001)
    bufferSize = 1024

    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)  # Receiving that the connection was successful and the client is permitted to start sending commands to drone
    msg = "Message from Server: {}".format(msgFromServer[0])
    print(msg)
