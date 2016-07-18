#!/usr/bin/env python
from socket import AF_INET, SOCK_DGRAM
import sys,os
import socket
import struct, time

'''
SERVIDORES DE ARGENTINA
server 3.ar.pool.ntp.org
server 3.south-america.pool.ntp.org
server 2.south-america.pool.ntp.org
'''

#def getNTPTime(host = "pool.ntp.org"):
def getNTPTime(host = "2.south-america.pool.ntp.org"):
	port = 123
	buf = 1024
	address = (host,port)
	msg = '\x1b' + 47 * '\0'

	# reference time (in seconds since 1900-01-01 00:00:00)
	TIME1970 = 2208988800L # 1970-01-01 00:00:00

	# connect to server
	client = socket.socket( AF_INET, SOCK_DGRAM)
	client.sendto(msg, address)
	msg, address = client.recvfrom( buf )
	t = struct.unpack( "!12I", msg )[10]
	t -= TIME1970
	return time.strftime('%Y-%m-%d %H:%M', time.localtime(t))

if __name__ == "__main__":
	t=getNTPTime()
	# Set de fecha
	os.system('date --set "%s"' %t)
