## Michal Ludvig <mludvig@logix.net.nz>
## http://www.logix.cz/michal/devel/sms-cli
## License: GPL Version 2

from logging import debug, info
from Sms.Exceptions import SmsError
import GenericHttp

class SmsDriver(GenericHttp.SmsDriver):
    def send(self, message, recipient):
        ret = super(self.__class__, self).send(message, recipient)
        arr = ret.split("\n")[0].split(" ", 1)
        if arr[0].startswith("ID"):
            info("SMS(Clickatell) sent to %s with ID: %s" % (recipient, arr[1]))
            return arr[1]
        raise SmsError("SMS(Clickatell): %s" % arr[1])

# vim:et:ts=4:sts=4:ai