
import socket
import json

from pprint import pprint

import dumps
import fort_fabric






class sender:

	def __init__(self):
		self.localhost = 'localhost'
		# self.ip = '178.91.254.41'
		self.ip = '127.0.0.1'
		self.port = 9090

		self.sourcelist = self.get_source_list() # loop list
		

	def get_source_list(self):
		with open('temp.json') as data_file:
			data = json.load(data_file)
		# pprint(data)
		return data

	def start(self):
		if self.sourcelist == []:
			print('Source list is empty')

		fabric = fort_fabric.fort_fabric()

		while True:

			print('start source loop')

			for dump in self.sourcelist:
				print('{}: {}'.format('Timestamp', dump['Timestamp']))
				# dump = self.sourcelist.next()

				msg = fabric.get_message(dump)
				self.send(msg)




	def send(self, msg):
		sock = socket.socket()
		sock.connect((self.ip, self.port))
		sock.send(msg)

		data = sock.recv(1024)
		sock.close()

		print('{}: {}'.format('after send', data))



def main():
	print('init')
	s = sender()
	print('start')
	s.start()


if __name__ == '__main__':
	main()