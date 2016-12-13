import arrow

from kottu import app

@app.template_filter('format_time')
def format_time(timestamp, format=None):
	"""Jinja filter to return human-readable/formatted time"""
	if(format == 'human'):
		return arrow.get(timestamp).humanize()
	else:
		return arrow.get(timestamp).format()

@app.template_filter('chilies')
def chilies(buzz):
	"""Jinja filter to return an integer number of chilies for postbuzz"""

	out = 1
	if(buzz > 0.55):
		out = 5
	elif(buzz > 0.35):
		out = 4
	elif(buzz > 0.15):
		out = 3
	elif(buzz > 0.01):
		out = 2

	return out