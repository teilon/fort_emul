#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

print('listn...')

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)




while True:
	conn, addr = sock.accept()
	print('connection:', addr)
	
	data = conn.recv(1024)
	print('data: {}'.format(data))
	# if not data:
	# 	break	
	conn.send(data.upper())


conn.close()