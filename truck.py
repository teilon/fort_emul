
import socket
import json

import dumps
import fort_fabric







class fort_fabric:
	def __init__(self):
		pass

	def get_message(self, dump):		
		return ''

class sender:

	def __init__(self):
		self.localhost = 'localhost'
		self.ip = '178.91.254.41'
		self.potr = '65400'

		self.sourcelist = get_source_list() # loop list

	def get_source_list():
		pass								# get source list from json

	def start(self):
		if self.sourcelist == []:
			print('Source list is empty')

		fabric = fort_fabric()

		while True:

			dump = self.sourcelist.next()
			msg = fabric.get_message(dump)
			send(msg)




	def send(self, msg):
		sock = socket.socket()
		sock.connect((self.localhost, self.potr))
		sock.send(msg)

		data = sock.recv(1024)
		sock.close()

		print(data)