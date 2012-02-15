## Author: Michal Ludvig <mludvig@logix.net.nz>
##         http://www.logix.cz/michal
## License: GPL Version 2

class SmsException(Exception):
    def __init__(self, message = ""):
        self.message = message

    def __str__(self):
        return unicode(self)

    def __unicode__(self):
        return self.message

    ## (Base)Exception.message has been deprecated in Python 2.6
    def _get_message(self):
        return self._message
    def _set_message(self, message):
        self._message = message
    message = property(_get_message, _set_message)

class SmsError(SmsException):
    pass

class SmsConfigError(SmsException):
    pass

# vim:et:ts=4:sts=4:ai
