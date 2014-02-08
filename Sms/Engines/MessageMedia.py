## Michal Ludvig <mludvig@logix.net.nz>
## http://www.logix.cz/michal/devel/sms-cli
## License: GPL Version 2

from Sms.Logger import *
from Sms.Exceptions import SmsError
from Sms.SimpleObjects import *
import GenericSoap

import os
import random
from datetime import datetime
try:
    from suds.client import Client, ObjectCache
except ImportError, e:
    raise SmsError("Module 'suds' not found. Please install python-suds package.")

replies_fetched = []
replies_fetched_timestamp = datetime.min
reports_fetched = []
reports_fetched_timestamp = datetime.min

def _timedelta_total_seconds(timedelta):
    # timedelta.total_seconds is not available in Python 2.6
    return timedelta.days * 86400 + timedelta.seconds + timedelta.microseconds/1000000

class SmsDriver(GenericSoap.SmsDriver):
    url = 'http://soap.m4u.com.au/?wsdl'

    def __init__(self, options = {}):
        GenericSoap.SmsDriver.__init__(self, options)

        # Soap Client
        cache = ObjectCache(location = "/tmp/suds.%d" % os.getuid())
        cache.setduration(days = 10)
        self.client = Client(self.url, cache = cache)

        # Authentication
        self.auth = self.client.factory.create('AuthenticationType')
        self.auth.userId = self.options['username']
        self.auth.password = self.options['password']

    def send(self, message):
        debug("MessageMedia.send([%s])" % ", ".join(message.recipients))

        # Message Type
        message_t = self.client.factory.create("MessageType")
        message_t.content = message.message
        message_t.deliveryReport = True
        for recipient in message.recipients:
            message_t.recipients.recipient.append(self.client.factory.create("RecipientType"))
            message_t.recipients.recipient[-1].value = recipient
            message_t.recipients.recipient[-1]._uid = random.randint(100000000, 999999999)

        # Container for multiple messages
        send_messages_t = self.client.factory.create("SendMessagesBodyType")
        send_messages_t.messages.message.append(message_t)

        # Send it out
        ret = self.client.service.sendMessages(self.auth, send_messages_t)

        error_recipients = []

        mids = []
        if 'errors' in dir(ret):
                for error in ret.errors.error:
                    for recipient in error.recipients.recipient:
                        debug("SMS(MessageMedia) failed to %s: %s" % (recipient.value, error._code))
                        error_recipients.append(recipient.value)
                        mids.append(SmsDeliveryStatus(message.message, recipient = recipient.value, despatched = False, comment = error._code))

        for recipient in message_t.recipients.recipient:
            if recipient.value not in error_recipients:
                debug("SMS(MessageMedia) sent to %s with ID: %s" % (recipient.value, recipient._uid))
                mids.append(SmsDeliveryStatus(message.message, recipient = recipient.value, despatched = True, mid = recipient._uid))
        return mids

    def receive(self, senders = [], in_reply_to = [], keep = False):
        global replies_fetched, replies_fetched_timestamp

        replies_raw = []

        replies_fetched_age = datetime.now() - replies_fetched_timestamp
        if _timedelta_total_seconds(replies_fetched_age) < 60:
            debug("SMS(MessageMedia) using cached replies: %s sec old" % (_timedelta_total_seconds(replies_fetched_age)))
        else:
            replies_fetched_timestamp = datetime.now()

            check_replies_t = self.client.service.checkReplies(self.auth)
            if not check_replies_t.replies:
                replies_fetched = []
            else:
                replies_fetched = check_replies_t.replies.reply
            debug("SMS(MessageMedia) received %d replies" % len(replies_fetched))
            for reply_t in replies_fetched:
                debug("SMS(MessageMedia) received reply sender=%s, uid=%s: %s" % (reply_t.origin, reply_t._uid, reply_t.content))

        # Fetch new messages
        if senders == [] and in_reply_to == []:
            replies_raw = replies_fetched
        else:
            for reply_t in replies_fetched:
                if str(reply_t._uid) in in_reply_to or reply_t.origin in senders:
                    debug("SMS(MessageMedia) matching reply sender=%s, uid=%s: %s" % (reply_t.origin, reply_t._uid, reply_t.content))
                    replies_raw.append(reply_t)

        # Delete messages from the gateway
        if replies_raw and not keep:
            confirm_replies_t = self.client.factory.create("ConfirmRepliesBodyType")
            for reply_t in replies_raw:
                confirm_replies_t.replies.reply.append(self.client.factory.create("ConfirmItemType"))
                confirm_replies_t.replies.reply[-1]._receiptId = str(reply_t._receiptId)
                debug("SMS(MessageMedia) deleting sender=%s, uid=%s: %s" % (reply_t.origin, reply_t._uid, reply_t.content))
            ret = self.client.service.confirmReplies(self.auth, confirm_replies_t)
            debug("SMS(MessageMedia) deleted %d messages" % ret._confirmed)

        replies = []
        for reply_t in replies_raw:
            replies.append(SmsMessage(message = reply_t.content, sender = reply_t.origin, mid = reply_t._uid, timestamp = reply_t.received))
        return replies

    def get_status(self, mids = [], keep = False):
        global reports_fetched, reports_fetched_timestamp

        report_to_status = {
            'delivered' : 'DELIVERED',
            'pending'   : 'TRANSIT',
            'failed'    : 'ERROR',
        }

        reports_raw = []

        reports_fetched_age = datetime.now() - reports_fetched_timestamp
        if _timedelta_total_seconds(reports_fetched_age) < 60:
            debug("SMS(MessageMedia) using cached delivery reports: %s sec old" % (_timedelta_total_seconds(reports_fetched_age)))
        else:
            reports_fetched_timestamp = datetime.now()

            check_reports_t = self.client.service.checkReports(self.auth)
            if not check_reports_t.reports:
                reports_fetched = []
            else:
                reports_fetched = check_reports_t.reports.report
            debug("SMS(MessageMedia) fetched %d delivery reports" % len(reports_fetched))
            for report_t in reports_fetched:
                debug("SMS(MessageMedia) report [%s] (uid=%s) %s: %s" % (report_t.timestamp, report_t._uid, report_t.recipient, report_t._status))

        if mids == []:
            reports_raw = reports_fetched
        else:
            for report_t in reports_fetched:
                if str(report_t._uid) in mids:
                    debug("SMS(MessageMedia) matching delivery report [%s] (uid=%s) %s: %s" % (report_t.timestamp, report_t._uid, report_t.recipient, report_t._status))
                    reports_raw.append(report_t)

        # Delete reports from the gateway
        if reports_raw and not keep:
            confirm_reports_t = self.client.factory.create("ConfirmReportsBodyType")
            for report_t in reports_raw:
                confirm_reports_t.reports.report.append(self.client.factory.create("ConfirmItemType"))
                confirm_reports_t.reports.report[-1]._receiptId = report_t._receiptId
            ret = self.client.service.confirmReports(self.auth, confirm_reports_t)
            debug("SMS(MessageMedia) deleted %d delivery reports" % ret._confirmed)

        statuses = []
        for report_t in reports_raw:
            try:
                status = report_to_status[report_t._status]
            except KeyError:
                status = "UNKNOWN"
            statuses.append(SmsDeliveryStatus(
                recipient = report_t.recipient,
                mid = report_t._uid,
                status = status,
                timestamp = report_t.timestamp))
        return statuses

# vim:et:sw=4:sts=4:ai:sta
