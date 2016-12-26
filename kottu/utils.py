import arrow, re
from collections import defaultdict

from kottu import app

UNICODE_BLOCKS = {
	'en': range(0x0000, 0x02AF),
	'si': range(0x0D80, 0x0DFF),
	'ta': range(0x0B80, 0x0BFF),
	'dv': range(0x0780, 0x07BF)
}

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

def getlang(text):
	"""
		Get language via Unicode range. Partially based on:
		https://github.com/kent37/guess-language/blob/master/guess_language/guess_language.py#L344
	"""

	langs = defaultdict(int)
	for c in text:
		if(c.isalpha()):
			for block in UNICODE_BLOCKS:
				if(ord(c) in UNICODE_BLOCKS[block]):
					langs[block] += 1

	if(langs):
		return max(langs, key=langs.get)
	else:
		return 'en'

def fetchthumb(item):
	"""
		Get the thumbnail image for an item if possible
	"""

	text = item.summary
	if 'content' in item:
		text = item.content[0].value

	# regex to get an image if available
	thumb_search = re.search('(https?:\/\/[\S]+\.(jpg|png|jpeg))', text, re.IGNORECASE)

	if thumb_search:
		return thumb_search.group(1)
	else:
		return None