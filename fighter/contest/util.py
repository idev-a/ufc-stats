from datetime import datetime

def _valid(val):
		if val:
			return val.strip()
		else:
			return ''

def strip_list1(arr):
	new_list = []
	for item in arr:
		if item and item.strip():
			new_list.append(_valid(item))
		# else:
			# new_list.append(' ')

	return new_list

def convert_date(date):
	return datetime.strptime(date, '%B %d, %Y').strftime('%Y-%m-%d')
