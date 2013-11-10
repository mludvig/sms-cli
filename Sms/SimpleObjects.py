## Michal Ludvig <mludvig@logix.net.nz>
## http://www.logix.cz/michal/devel/sms-cli
## License: GPL Version 2

from datetime import datetime

__all__ = []

__all__.append("SmsMessage")
class SmsMessage(object):
    def __init__(self, message, sender = None, recipients = [], mid = None, timestamp = None):
        self.message = message
        self.sender = sender
        self.recipients = recipients
        self.mid = mid
        self.timestamp = timestamp or datetime.now()

    def __unicode__(self):
        return self.message

__all__.append("SmsDeliveryStatus")
class SmsDeliveryStatus(object):
    statuses = [ "UNKNOWN", "TRANSIT", "ERROR", "EXPIRED", "DELIVERED", "PENDING" ]
    def __init__(self, message = "", recipient = None, despatched = False, status = None, mid = None, timestamp = None, comment = "", **kwargs):
        self.message = message
        self.recipient = recipient
        self.despatched = despatched
        self.mid = mid
        self.status = status or (self.despatched and "TRANSIT" or "ERROR")
        self.timestamp = timestamp or datetime.now()
        self.comment = comment
        self.xxkwargs = kwargs
        assert(self.status in SmsDeliveryStatus.statuses)

    def __str__(self):
        return "%s - %s - %s - %s" % (self.recipient, self.mid, self.status, self.timestamp)

    def __getitem__(self, item):
        return self.__getattribute__(item)
