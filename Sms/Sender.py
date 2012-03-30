## Michal Ludvig <mludvig@logix.net.nz>
## http://www.logix.cz/michal/devel/sms-cli
## License: GPL Version 2

from Config import Config
from Exceptions import *
from Logger import *

class SmsStatus(object):
    def __init__(self, code, descr = "", verbose = ""):
        assert(code in [ "UNKNOWN", "TRANSIT", "ERROR", "EXPIRED", "DELIVERED" ])
        self.code = code
        self.descr = descr
        self.verbose = verbose

    def __str__(self):
        return "%s - %s" % (self.code, self.descr)

class SmsSender(object):
    def __init__(self, recipients = [], engine_options = {}, **kwargs):
        assert(type(recipients) == type([]))
        debug("Importing engine: %s" % Config().engine)
        driver_module = __import__("Sms.Engines." + Config().engine, fromlist = ["Sms.Engines"])
        self._driver = driver_module.SmsDriver(options = Config().engine_options(), **kwargs)
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
        assert(type(recipients) == type([]))
        if not message:
            message = self._message
            self.clearMessage()
        if not recipients:
            recipients = self._recipients

        assert(message and recipients)

        ids = []
        try:
            if 'sendMulti' in dir(self._driver):
                ids = self._driver.sendMulti(message, recipients)
            else:
                for recipient in recipients:
                    ids.append(self._driver.sendOne(message, recipient))
        except SmsError, e:
            return (False, e, ids)

        return (True, ids)

    def get_status(self, messageid):
        return SmsStatus("UNKNOWN", "Not implemented")

# vim: et:sw=4:sts=4:sta:ai:
