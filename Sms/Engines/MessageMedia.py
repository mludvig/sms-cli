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

    def sendMulti(self, message, recipients):
        client = Client(self.url, cache = self.cache)

        # Authentication
        auth = client.factory.create('AuthenticationType')
        auth.userId = self.options['username']
        auth.password = self.options['password']

        # Message Type
        message_t = client.factory.create("MessageType")
        message_t.content = message
        message_t.deliveryReport = True
        for recipient in recipients:
            message_t.recipients.recipient.append(client.factory.create("RecipientType"))
            message_t.recipients.recipient[-1].value = recipient
            message_t.recipients.recipient[-1]._uid = random.randint(100000000, 999999999)

        # Container for multiple messages
        send_messages_t = client.factory.create("SendMessagesBodyType")
        send_messages_t.messages.message.append(message_t)

        # Send it out
        ret = client.service.sendMessages(auth, send_messages_t)

        error_recipients = []
        for error in ret.errors.error:
            for recipient in error.recipients.recipient:
                warning("SMS(MessageMedia) failed to %s: %s" % (recipient.value, error._code))
                error_recipients.append(recipient.value)

        for recipient in message_t.recipients.recipient:
            if recipient.value not in error_recipients:
                info("SMS(MessageMedia) sent to %s with ID: %s" % (recipient.value, recipient._uid))

# vim:et:sw=4:sts=4:ai:sta
