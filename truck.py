
import socket
import json
from datetime import datetime


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
				
				# dump = self.sourcelist.next()
				dt_start = datetime.utcnow()

				msg, num = fabric.get_message(dump)
				
				self.send(msg)

				dt_end = datetime.utcnow()
				dt_delta = dt_end - dt_start

				print('{}: {} | {:10} | {}'.format(
					'Timestamp', 
					dump['Timestamp'], 
					num,
					dt_delta))





	def send(self, msg):
		sock = socket.socket()
		sock.connect((self.ip, self.port))
		sock.send(msg)

		data = sock.recv(1024)
		sock.close()


def main():
	s = sender()
	s.start()


if __name__ == '__main__':
	main()