## Michal Ludvig <mludvig@logix.net.nz>
## http://www.logix.cz/michal/devel/sms-cli
## License: GPL Version 2

import urllib
import urllib2

from Exceptions import *
from GenericSmsDriver import GenericSmsDriver

class SmsDriver(GenericSmsDriver):
    def send(self, message, recipient):
        url = self.options['url_pattern'].strip('"\'') % { 'message' : urllib.quote(message), 'recipient' : recipient }
        u = urllib2.urlopen(url)
        if u.code != 200:
            raise SmsError("HTTP Return code = %d" % u.code)
        return u.read()

# vim:et:ts=4:sts=4:ai
