from logging import debug, error
from Config import Config

class SmsError(Exception):
	pass

class SmsSender(object):
	def __init__(self, recipients = [], **kwargs):
		driver_module = __import__(Config().sms_engine.replace(".","/"))
		self._driver = driver_module.SmsDriver(**kwargs)
		self._recipients = recipients
		self._message = ""

	def addRecipient(self, recipient):
		self._recipients.append(recipient)

	def clearRecipients(self):
		self._recipients = recipients

	def addMessage(self, message):
		if self._message:
			self._message += "\n"
		self._message += message

	def clearMessage(self):
		self._message = ""

	def send(self, message = None, recipients = []):
		if not message:
			message = self._message
			self.clearMessage()
		if not recipients:
			recipients = self._recipients

		assert(message and recipients)

		try:
			try:
				self._driver.sendMulti(message, recipients)
			except AttributeError:
				for recipient in recipients:
					self._driver.send(message, recipient)
		except SmsError, e:
			error(str(e))
			return False

		return True

