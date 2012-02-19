## Michal Ludvig <mludvig@logix.net.nz>
## http://www.logix.cz/michal/devel/sms-cli
## License: GPL Version 2

import urllib
import urllib2

from Sms.Exceptions import *
from Sms.GenericSmsDriver import GenericSmsDriver
from Sms.Logger import *

class SmsDriver(GenericSmsDriver):
    url_pattern = None

    def __init__(self, options):
        GenericSmsDriver.__init__(self, options)
        if not self.url_pattern:
            try:
                self.url_pattern = self.options['url_pattern'].strip('"\'')
            except KeyError, e:
                raise SmsConfigError("GenericHttp driver requires 'url_pattern' option")

    def sendOne(self, message, recipient):
        debug("GenericHttp.sendOne(%s)" % recipient)
        all_options = { 'message' : urllib.quote(message), 'recipient' : recipient }
        all_options.update(self.options)
        url = self.url_pattern % all_options
        debug("GenericHttp: url: %s" % url)
        u = urllib2.urlopen(url)
        debug("GenericHttp: ret_code: %s" % u.code)
        if u.code != 200:
            raise SmsError("HTTP Return code = %d" % u.code)
        ret_data = u.read().strip()
        debug("GenericHttp: ret_data: %s" % ret_data)
        return ret_data

# vim: et:sw=4:sts=4:sta:ai:
