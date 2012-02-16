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

    def send(self, message, recipient):
        client = Client(self.url, cache = self.cache)

        # Authentication
        auth = client.factory.create('AuthenticationType')
        auth.userId = self.options['username']
        auth.password = self.options['password']

        # Message ID
        message_id = random.randint(100000000, 999999999)

        # Message Type
        message_t = client.factory.create("MessageType")
        message_t.content = message
        message_t.deliveryReport = True
        message_t.recipients.recipient.append(client.factory.create("RecipientType"))
        message_t.recipients.recipient[-1].value = recipient
        message_t.recipients.recipient[-1]._uid = message_id

        # Container for multiple messages
        send_messages_t = client.factory.create("SendMessagesBodyType")
        send_messages_t.messages.message.append(message_t)

        # Send it out
        ret = client.service.sendMessages(auth, send_messages_t)

        if ret._sent > 0:
            info("SMS(MessageMedia) sent to %s with ID: %s" % (recipient, message_id))
            return message_id
        if ret._failed > 0:
            warning("SMS(MessageMedia) failed to %s: %s" % (recipient, ret.errors.error[0]._code))

# vim:et:ts=4:sts=4:ai
