from datetime import datetime
import re
import math

class fort_fabric():

	def __init__(self):
		self.dumps = {}

	def get_message(self, **input):
		dump = input
		num = _get_last_num(dump['imei'])
		msg = '{}{}{}{}{}'.format(
			_get_title(dump['imei']),
			_get_info(),
			_get_gnss(dump['latitude'], dump['longitude'], dump['altitude'], dump['speed']),
			_get_io(),
			_get_end(num)
			)
		return self._set_length_to_message(msg)

	def _get_title(self, imei):
		title = 'DA' + '02' + '0B'
		length = 'GGGG'
		dump_imei = '5D' + imei

		return title + length + dump_imei

	def _get_info(self):
		title = '1F'
										# 'ddMMyyHHmmss'
		utc = datetime.utcnow()
		cur_datetime = '16' + datetime.strptime(utc, '%d%m%y%H%M%S')
		length = 'HH'
		result = title + length + cur_datetime
		return _set_length_to_section(result)

	def _get_gnss(self, lat, lon, alt, speed):
		title = '2F'
		length = 'HH'
		state = '23'
		gnss = '42' + self._get_lat_lon(lat) + self._get_lat_lon(lon) + self._get_speed(speed) + self._get_heading() + self._get_alt(alt)
		cur_datetime = '16' + datetime.strptime(utc, '%d%m%y%H%M%S')
		result = title + length + state + gnss + cur_datetime

		return _set_length_to_section(result)

	def _get_io(self):
		return '4F06120000220000'

	def _get_end(self, num):
		return 'AA55' + self._get_hex(num)

	def _get_last_num(self, imei):
		_step, _max, _first = 1, 255, 0
		last = self.dumps[imei]
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
		replacement = _check_hex('00' + self._get_hex(length))
		pattern = 'GGGG'

		result = re.sub(pattern, replacement)
		return result

	def _set_length_to_section(self, input):
		length = len(input) / 2 - 2
		replacement = _check_hex(self._get_hex(length))
		pattern = 'HH'

		result = re.sub(pattern, replacement)
		return result


	def _get_hex(self, value):
		h = hex(value)
		return h[2:].upper()


	def _get_le(self, value):
		return self._get_hex(value)

	def _get_speed(self, value):
		return self._get_le(value * 10)

	def _get_heading(self):
		return '0000'

	def _get_alt(self, value):
		return self._get_le(value)

	def _get_out_gradus(self, value):
		flat = value - math.floor(value)
		return (math.floor(value) + (flat * 0.6)) * 100

	def _get_lat_lon(self, value):
		value = _get_out_gradus(value)
		return self._get_hex(value)

	def _check_hex(self, input):
		result = input
		if len(input) % 2 != 0:
			result = '0' + result
		return result