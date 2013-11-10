## Michal Ludvig <mludvig@logix.net.nz>
## http://www.logix.cz/michal/devel/sms-cli
## License: GPL Version 2

from Sms.Logger import *
from Sms.Exceptions import SmsError
from Sms.SimpleObjects import SmsDeliveryStatus
import GenericHttp

class SmsDriver(GenericHttp.SmsDriver):
    url_pattern = "https://api.clickatell.com/http/sendmsg?api_id=%(api_id)s&user=%(username)s&password=%(password)s&to=%(recipient)s&text=%(message)s"

    def sendOne(self, message, recipient):
        debug("Clickatell.sendOne(%s)" % recipient)
        ret = GenericHttp.SmsDriver.sendOneLowLevel(self, message, recipient)
        arr = ret.split("\n")[0].split(" ", 1)
        if arr[0].startswith("ID"):
            debug("SMS(Clickatell) sent to %s with ID: %s" % (recipient, arr[1]))
            return SmsDeliveryStatus(message, recipient = recipient, despatched = True, mid = arr[1])
        else:
            debug("SMS(Clickatell) failed to %s: %s" % (recipient, ret))
            return SmsDeliveryStatus(message, recipient = recipient, despatched = False, comment = ret)

# vim: et:sw=4:sts=4:sta:ai:
