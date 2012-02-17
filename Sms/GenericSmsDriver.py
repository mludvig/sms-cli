## Michal Ludvig <mludvig@logix.net.nz>
## http://www.logix.cz/michal/devel/sms-cli
## License: GPL Version 2

from Logger import *
from Exceptions import *

class GenericSmsDriver(object):
    def __init__(self, options = {}):
        self.set_options(options)

    def set_options(self, options):
        debug("Setting options to: %r" % options)
        self.options = options

# vim:et:ts=4:sts=4:ai
