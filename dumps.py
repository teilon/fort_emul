class dump:

	def __init__(self):
		self._deviceid = ''
		self._imei = ''
		self._timestamp = 0
		self._latitude = 0
		self._longitude = 0
		self._altitude = 0
		self._speed = 0
		self._heading = 0

		self.prev = None
		self.next = None


	# {
	# 'Deviceid':'804',
	# 'Imei':'fort_0354868052847854',
	# 'Timestamp':'1493196245',
	# 'Latitude':'43.2359619140625',
	# 'Longitude':'76.8729410807292',
	# 'Altitude':'840',
	# 'Speed':'1.5',
	# 'Heading':'172'
	# }

class dump_list:

	def __init__(self):
		self._dumps = []

	def __iter__(self):
		return list_iterator(self)

	def __len__(self):
		return self._dumps.length

	def __add__(self, value):
		first, last = self._dumps[0, -1]		
		self._dumps.append(value)

		first.prev = value
		last.next = value

		value.prev = last
		value.next = first


class list_iterator:
	def __init__(self, list_instance):
		self._list = list_instance
		self.next_value = list_instance[0]

	def __iter__(self):
		return self

	def __next__(self):		
		if self.next_value == None:
			raise StopIteration

		result = self.next_value
		self.next_value = self.next_value.next

		return result