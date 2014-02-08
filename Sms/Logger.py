## Michal Ludvig <mludvig@logix.net.nz>
## http://www.logix.cz/michal/devel/sms-cli
## License: GPL Version 2

import sys
import logging
import unicodedata

__all__ = []

_logger = logging.getLogger("sms-cli")

def logger_init(level):
    global _logger

    # create logger
    _logger = logging.getLogger("sms-cli")
    _logger.setLevel(level)

    if sys.stderr.isatty():
        # create stderr handler only on console
        stderr_handler = logging.StreamHandler()
        stderr_handler.setLevel(logging.DEBUG)
        stderr_formatter = logging.Formatter('%(levelname)s: %(message)s')
        stderr_handler.setFormatter(stderr_formatter)
        _logger.addHandler(stderr_handler)
    else:
        # not on a console -> syslog handler
        syslog_handler = logging.handlers.SysLogHandler(facility=logging.handlers.SysLogHandler.LOG_USER, address='/dev/log')
        syslog_handler.setLevel(logging.DEBUG)
        syslog_formatter = logging.Formatter('sms-cli: %(levelname)s: %(message)s')
        syslog_handler.setFormatter(syslog_formatter)
        _logger.addHandler(syslog_handler)

    # remove parent to avoid double-logging
    _logger.parent = None
__all__.append("logger_init")

def logger_set_level(level):
    _logger.setLevel(level)
__all__.append("logger_set_level")

def deunicode(msg):
    if type(msg) == unicode:
        return unicodedata.normalize('NFKD', msg).encode('ascii','ignore')
    else:
        return str(msg)

def debug(message):
	_logger.debug(deunicode(message))
__all__.append("debug")

def info(message):
	_logger.info(deunicode(message))
__all__.append("info")

def warning(message):
	_logger.warning(deunicode(message))
__all__.append("warning")

def error(message):
	_logger.error(deunicode(message))
__all__.append("error")

def critical(message):
	_logger.critical(deunicode(message))
__all__.append("critical")

logger_init(logging.DEBUG)

if __name__ == "__main__":
    info("Before loglevel - should not be displayed")
    logger_init(logging.INFO)
    info("Default format")
    logger_init(logging.DEBUG, format='%(levelname)s: %(message)s')
    debug("Our formar")
    error("Error, really!")

# vim:et:ts=4:sts=4:ai
