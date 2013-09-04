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

    def send(self, message):
        return self._driver.send(message)

    def receive(self, senders = [], in_reply_to = [], keep = False):
        assert(type(senders) == list)
        assert(type(in_reply_to) == list)

        if 'receive' not in dir(self._driver):
            raise SmsError(message = "Not implemented in engine: %s" % self._driver.__module__)

        return self._driver.receive(senders = senders, in_reply_to = in_reply_to, keep = keep)

    def get_status(self, messageid):
        return SmsStatus("UNKNOWN", "Not implemented")

# vim: et:sw=4:sts=4:sta:ai:
