import urllib
import urllib2

## Must be full path because this module is imported via __import__()
from Config import Config
from Sender import SmsError

class SmsDriver(object):
	def __init__(self):
		self._url_pattern = Config().sms_url_pattern

	def send(self, message, recipient):
		url = self._url_pattern.strip('"\'') % { 'message' : urllib.quote(message), 'recipient' : recipient }
		u = urllib2.urlopen(url)
		if u.code != 200:
			raise SmsError("HTTP Return code = %d" % u.code)
		return u.read()
