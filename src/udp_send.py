import socket

udp_ip = "10.63.57.2"
# RoboRIO ip address: 10.TE.AM.2

udp_port = 5800
# Available bi-directionl UDP/TCP ports on RoboRIO: 5800-5810


local_port = 5005


sock_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_s.bind(('0.0.0.0', local_port))
# binds to local port meaning that sock_s.sendto()
# will always send from RPi UDP @ local_port

while True:
    s_data = input("Send message: ")
    sock_s.sendto(s_data.encode('utf-8'), (udp_ip, udp_port))
    # encodes s_data bytes as uft-8 and sends to device with udp_ip at udp_port

    data, addr = sock_s.recvfrom(1024)
    # retrives data from the port sock_s in bound to -> local_port
    print("received message: %s" % data.decode('utf-8'))
    # before printing message the bytes must be decoded to string format so it can be printed
    # equaivalent to Java .toString() from bytes