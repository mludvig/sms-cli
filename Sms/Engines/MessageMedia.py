## Michal Ludvig <mludvig@logix.net.nz>
## http://www.logix.cz/michal/devel/sms-cli
## License: GPL Version 2

from Sms.Logger import *
from Sms.Exceptions import SmsError
import GenericSoap

import random
from suds.client import Client

class SmsDriver(GenericSoap.SmsDriver):
    url = 'http://soap.m4u.com.au/?wsdl'

    def __init__(self, options = {}):
        GenericSoap.SmsDriver.__init__(self, options)

        # Soap Client
        self.client = Client(self.url, cache = self.cache)

        # Authentication
        self.auth = self.client.factory.create('AuthenticationType')
        self.auth.userId = self.options['username']
        self.auth.password = self.options['password']

    def sendMulti(self, message, recipients):
        debug("MessageMedia.sendMulti([%s])" % ", ".join(recipients))

        # Message Type
        message_t = self.client.factory.create("MessageType")
        message_t.content = message
        message_t.deliveryReport = True
        for recipient in recipients:
            message_t.recipients.recipient.append(self.client.factory.create("RecipientType"))
            message_t.recipients.recipient[-1].value = recipient
            message_t.recipients.recipient[-1]._uid = random.randint(100000000, 999999999)

        # Container for multiple messages
        send_messages_t = self.client.factory.create("SendMessagesBodyType")
        send_messages_t.messages.message.append(message_t)

        # Send it out
        ret = self.client.service.sendMessages(self.auth, send_messages_t)

        error_recipients = []

        if 'errors' in dir(ret):
                for error in ret.errors.error:
                    for recipient in error.recipients.recipient:
                        warning("SMS(MessageMedia) failed to %s: %s" % (recipient.value, error._code))
                        error_recipients.append(recipient.value)

        ids = []
        for recipient in message_t.recipients.recipient:
            if recipient.value not in error_recipients:
                info("SMS(MessageMedia) sent to %s with ID: %s" % (recipient.value, recipient._uid))
                ids.append(recipient._uid)

        return ids

    def sendOne(self, message, recipient):
        ids = self.sendMulti(message, [recipient])
        try:
            return ids[0]
        except:
            return None

# vim:et:sw=4:sts=4:ai:sta
