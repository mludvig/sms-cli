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

__all__.append("SmsSendStatus")
class SmsSendStatus(object):
        def __init__(self, message, recipient = None, recipients = [], despatched = True, mid = None, comment = "", **kwargs):
                if recipient:
                        if not recipients:
                                recipients = [ recipient ]
                        else:
                                recipients.append(recipient)
                self.message = message
                self.recipients = recipients
                self.despatched = despatched
                self.mid = mid
                self.comment = comment
                self.xxkwargs = kwargs

__all__.append("SmsDeliveryStatus")
class SmsDeliveryStatus(object):
    statuses = [ "UNKNOWN", "TRANSIT", "ERROR", "EXPIRED", "DELIVERED", "PENDING" ]

    def __init__(self, recipient = None, mid = None, status = "UNKNOWN", timestamp = None, comment = ""):
        assert(status in SmsDeliveryStatus.statuses)
        self.recipient = recipient
        self.mid = mid
        self.status = status
        self.timestamp = timestamp or datetime.now()
        self.comment = comment

    def __str__(self):
        return "%s - %s - %s - %s" % (self.recipient, self.mid, self.status, self.timestamp)

    def __getitem__(self, item):
        return self.__getattribute__(item)
