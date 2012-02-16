## Michal Ludvig <mludvig@logix.net.nz>
## http://www.logix.cz/michal/devel/sms-cli
## License: GPL Version 2

import os
import logging
from Sms.Exceptions import *
from Sms.GenericSmsDriver import GenericSmsDriver

try:
    from suds.client import ObjectCache
except ImportError, e:
    raise SmsError("Module 'suds' not found. Please install python-suds package.")

class SmsDriver(GenericSmsDriver):
    cache = None
    def __init__(self, options = {}):
        GenericSmsDriver.__init__(self, options)
        self.cache = ObjectCache()
        self.cache.setlocation(location = "/tmp/sms-cli.suds.%d" % os.getuid())
        self.cache.setduration(days = 10)

# vim:et:ts=4:sts=4:ai
