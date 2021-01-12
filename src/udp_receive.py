import socket

udp_ip = "192.168.86.44"
# laptop ipv4 address
udp_port = 5005
# udp port on laptop inbound rule

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((udp_ip, udp_port))
while True:
    data, addr = sock.recvfrom(1024)
    print("received message: %s" % data)