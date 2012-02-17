## Michal Ludvig <mludvig@logix.net.nz>
## http://www.logix.cz/michal/devel/sms-cli
## License: GPL Version 2

from Sms.Logger import *
from Sms.Exceptions import SmsError
import GenericHttp

class SmsDriver(GenericHttp.SmsDriver):
    url_pattern = "https://api.clickatell.com/http/sendmsg?api_id=%(api_id)s&user=%(user)s&password=%(password)s&to=%(recipient)s&text=%(message)s"

    def sendOne(self, message, recipient):
        debug("Clickatell.sendOne(%s)" % recipient)
        ret = GenericHttp.SmsDriver.sendOne(self, message, recipient)
        arr = ret.split("\n")[0].split(" ", 1)
        if arr[0].startswith("ID"):
            info("SMS(Clickatell) sent to %s with ID: %s" % (recipient, arr[1]))
        else:
            warning("SMS(Clickatell) failed to %s: %s" % (recipient, ret))

# vim: et:sw=4:sts=4:sta:ai:
