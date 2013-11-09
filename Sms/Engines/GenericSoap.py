## Michal Ludvig <mludvig@logix.net.nz>
## http://www.logix.cz/michal/devel/sms-cli
## License: GPL Version 2

import os
import logging
from Sms.Exceptions import *
from Sms.GenericSmsDriver import GenericSmsDriver

class SmsDriver(GenericSmsDriver):
    def __init__(self, options = {}):
        GenericSmsDriver.__init__(self, options)

# vim:et:ts=4:sts=4:ai
