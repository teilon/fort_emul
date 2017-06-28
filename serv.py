#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

sock = socket.socket()
sock.bind(('', 65400))
sock.listen(1)
conn, addr = sock.accept()

print('connection:\t', addr)

while True:
	data = conn.recv(1024)
	if not data:
		break
	conn.send(data.upper())

conn.close()