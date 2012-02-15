from logging import debug, info
from Exceptions import *

class GenericSmsDriver(object):
	def __init__(self, options = {}):
		self.set_options(options)

	def set_options(self, options):
		debug("Setting options to: %r" % options)
		self.options = options

	def send(self, message, recipient):
		raise SmsConfigError("GenericSmsDriver is not intended for direct use")
