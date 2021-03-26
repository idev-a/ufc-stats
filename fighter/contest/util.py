from datetime import datetime, timedelta

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
	return (datetime.strptime(date, '%B %d, %Y %H:%M:%S') - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')

def html2png(body=None):
	body = """
	<html>
		<head>
		<meta name="imgkit-format" content="png"/>
		<meta name="imgkit-orientation" content="Landscape"/>
		</head>
		Hello World!
		</html>
	"""

	imgkit.from_string(body, 'out.png')