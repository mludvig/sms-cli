## Michal Ludvig <mludvig@logix.net.nz>
## http://www.logix.cz/michal/devel/sms-cli
## License: GPL Version 2

import logging

__all__ = []

_logger = logging.getLogger("sms-cli")

def logger_init(level, format = '%(levelname)s: %(message)s'):
    global _logger

    # create logger
    _logger = logging.getLogger("sms-cli")
    _logger.setLevel(level)

    # create console handler and set level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(format)
    ch.setFormatter(formatter)

    # add ch to logger
    _logger.addHandler(ch)

    # remove parent to avoid double-logging
    _logger.parent = None
__all__.append("logger_init")

def logger_set_level(level):
    _logger.setLevel(level)
__all__.append("logger_set_level")

def debug(message):
	_logger.debug(message)
__all__.append("debug")

def info(message):
	_logger.info(message)
__all__.append("info")

def warning(message):
	_logger.warning(message)
__all__.append("warning")

def error(message):
	_logger.error(message)
__all__.append("error")

def critical(message):
	_logger.critical(message)
__all__.append("critical")

if __name__ == "__main__":
    info("Before loglevel - should not be displayed")
    logger_init(logging.INFO)
    info("Default format")
    logger_init(logging.DEBUG, format='%(levelname)s: %(message)s')
    debug("Our formar")
    error("Error, really!")

# vim:et:ts=4:sts=4:ai
