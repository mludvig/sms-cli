## Michal Ludvig <mludvig@logix.net.nz>
## http://www.logix.cz/michal/devel/sms-cli
## License: GPL Version 2

from datetime import datetime

__all__ = [ "SmsMessage" ]

class SmsMessage(object):
        def __init__(self, message, sender = None, recipients = [], mid = None, timestamp = None):
                self.message = message
                self.sender = sender
                self.recipients = recipients
                self.mid = mid
                self.timestamp = timestamp or datetime.now()

        def __unicode__(self):
                return self.message

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
