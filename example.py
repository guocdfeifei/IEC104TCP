from iec104client import *
from iec104_tcp_packets import *

server_ip = '192.168.3.5'
client = iec104_tcp_client(server_ip)
for p in plist:
    print client.sendOne(p)
	




