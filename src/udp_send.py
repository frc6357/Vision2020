import socket

udp_ip = "192.168.86.44"
# laptop ipv4 address
udp_port = 5005
# udp port on laptop inbound rule

local_ip = "192.168.86.37"
# RPi ip address
# I think I can delete this

local_port = 9999
# registered port on RPi
# 0 through 1023: Well Known Ports
# 1024 through 49151: Registered Ports
# 49152 through 65535: Dynamic and/or Private Ports

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