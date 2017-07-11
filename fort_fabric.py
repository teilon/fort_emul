from datetime import datetime
import re
import math

from pprint import pprint

class fort_fabric():

	def __init__(self):
		print('fort_fabric init')

		# for lastnumbers
		# imei : lastnumber
		self.dumps = {}

	def get_message(self, input):

		# pprint(input)

		dump = input
		if self.dumps.get(dump['Imei']) == None:
			self.dumps[dump['Imei']] = 0

		num = self._get_last_num(dump['Imei'])
		msg = '{}{}{}{}{}'.format(
			self._get_title(dump['Imei']),
			self._get_info(),
			self._get_gnss(dump['Latitude'], dump['Longitude'], dump['Altitude'], dump['Speed']),
			self._get_io(),
			self._get_end(num)
			)
		return self._set_length_to_message(msg)

	def _get_title(self, imei):
		title = 'DA' + '02' + '0B'
		length = 'GGGG'
		dump_imei = '5D' + re.search(r'\d+', imei).group(0)

		return title + length + dump_imei

	def _get_info(self):
		title = '1F'
										# 'ddMMyyHHmmss'
		# utc = '{}'.format(datetime.utcnow())
		# cur_datetime = '16{}'.format(datetime.strptime(utc, '%d%m%y%H%M%S'))

		utc = datetime.utcnow()
		cur_datetime = '16{:0>2}{:0>2}{:0>2}{:0>2}{:0>2}{:0>2}'.format(
			utc.day, 
			utc.month, 
			str(utc.year)[-2:], 
			utc.hour, 
			utc.minute, 
			utc.second
			)

		length = 'HH'
		result = title + length + cur_datetime
		return self._set_length_to_section(result)

	def _get_gnss(self, lat, lon, alt, speed):
		title = '2F'
		length = 'HH'
		state = '23'
		gnss = '42' + self._get_lat_lon(lat) + self._get_lat_lon(lon) + self._get_speed(speed) + self._get_heading() + self._get_alt(alt)
		
		# cur_datetime = '16' + datetime.strptime(utc, '%d%m%y%H%M%S')
		utc = datetime.utcnow()
		cur_datetime = '16{:0>2}{:0>2}{:0>2}{:0>2}{:0>2}{:0>2}'.format(
			utc.day, 
			utc.month, 
			str(utc.year)[-2:], 
			utc.hour, 
			utc.minute, 
			utc.second
			)

		result = title + length + state + gnss + cur_datetime

		return self._set_length_to_section(result)

	def _get_io(self):
		return '4F06120000220000'

	def _get_end(self, num):
		return 'AA55' + self._get_hex(num)

	def _get_last_num(self, imei):

		print('_get_last_num start')

		_step, _max, _first = 1, 255, 0
		last = self.dumps[imei]

		print('last: {}'.format(last))

		if last != None:
			if last < _max:
				self.dumps[imei] = last + _step
			else:
				self.dumps[imei] = _first
		else:
			self.dumps[imei] = _first

		return self.dumps[imei]



	def _set_length_to_message(self, input):
		length = len(input) / 2
		replacement = self._check_hex('00' + self._get_hex(length))
		pattern = 'GGGG'

		result = re.sub(pattern, replacement, input)
		return result

	def _set_length_to_section(self, input):

		length = len(input) / 2 - 2
		replacement = self._check_hex(self._get_hex(length))
		pattern = 'HH'

		result = re.sub(pattern, replacement, input)
		return result


	def _get_hex(self, value):		
		h = hex(int(value))
		return h[2:].upper()


	def _get_le(self, value):
		return self._get_hex(value)

	def _get_speed(self, value):
		return self._get_le(float(value) * 10)

	def _get_heading(self):
		return '0000'

	def _get_alt(self, value):
		return self._get_le(value)

	def _get_out_gradus(self, value):
		# flat = value - math.floor(value_)
		value_ = float(value)
		flat = int(value_)
		return (math.floor(value_) + (flat * 0.6)) * 100

	def _get_lat_lon(self, value):
		value_ = self._get_out_gradus(value)
		return self._get_hex(int(value_))

	def _check_hex(self, input):
		result = input
		if len(input) % 2 != 0:
			result = '0' + result
		return result