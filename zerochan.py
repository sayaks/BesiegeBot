import urllib.request
import requests

import re

picsite = 'https://www.zerochan.net/{0}?s=random'


def get_pic(tag, attempts = 1):
	imagesource = __FindPic(tag)
	if imagesource == None:
		return None
	for i in range(attempts):
		image = __ExtractPic(imagesource)
		if image != None:
			return (imagesource, image)	
	
	return None

def __FindPic(tag):
	try:
		with urllib.request.urlopen(picsite.format(tag)) as response:
			if response.status != 200:
				print("Site returned status %d" % response.status)
				return None
			text = response.read().decode()
			text = text.split('<ul id="thumbs2">')[1]
			text = text.split('"')[1]
	except Exception as e:
		print(e)
		return None
	return 'https://www.zerochan.net' + text


def __ExtractPic(url):
	try:
		with urllib.request.urlopen(url) as response:
			if response.status != 200:
				print("Site returned status %d" % response.status)
				return None
			text = response.read().decode()
			text = text.split('&quot;')[3]
			text = text.replace('.240.', '.full.')
			print(text)
	except Exception as e:
		print(e)
		return None
	return text
