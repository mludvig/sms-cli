## Michal Ludvig <mludvig@logix.net.nz>
## http://www.logix.cz/michal/devel/sms-cli
## License: GPL Version 2

from Sms.Logger import *
from Sms.Exceptions import SmsError
import GenericSoap

from suds.client import Client

class SmsDriver(GenericSoap.SmsDriver):
    url = 'http://soap.m4u.com.au/?wsdl'

    def send(self, message, recipient):
        client = Client(self.url, cache = self.cache)

        # Authentication
        auth = client.factory.create('AuthenticationType')
        auth.userId = self.options['username']
        auth.password = self.options['password']

        # Message Type
        message_t = client.factory.create("MessageType")
        message_t.content = message
        message_t.deliveryReport = True
        message_t.recipients.recipient.append(client.factory.create("RecipientType"))
        message_t.recipients.recipient[-1].value = recipient
        # message_t.recipients.recipient[-1]._uid = recipient + rand()

        # Container for multiple messages
        send_messages_t = client.factory.create("SendMessagesBodyType")
        send_messages_t.messages.message.append(message_t)

        print send_messages_t

        # Send it out
        ret = client.service.sendMessages(auth, send_messages_t)

        print ret

# vim:et:ts=4:sts=4:ai
