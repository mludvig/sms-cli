#!/usr/bin/env python

# sms.py - command line SMS sender
# Michal Ludvig <michal@logix.cz>
# http://www.logix.cz

import os
import sys

import datetime
import logging

from optparse import OptionParser
from logging import debug, info, warning, error

from Sms.Config import Config
from Sms.Sender import SmsSender

try:
	default_config_file=os.getenv("HOME")+"/.smscfg"
except:
	default_config_file="<unset>"

## Parse command line options
default_verbosity = Config().verbosity
optparser = OptionParser()
optparser.set_defaults(config=default_config_file)
optparser.set_defaults(verbosity = default_verbosity)

optparser.add_option("-c", "--config", dest="config", metavar="FILE", help="Config file name. Defaults to %default")
optparser.add_option(      "--debug", dest="verbosity", action="store_const", const=logging.DEBUG, help="Enable debug output.")
optparser.add_option(      "--quiet", dest="verbosity", action="store_const", const=logging.WARNING, help="Suppres most messages. Only Warnings and Errors are printed.")
optparser.add_option(      "--dump-config", dest="dump_config", action="store_true", help="Dump current configuration after parsing config files and command line options and exit.")
optparser.add_option("-r", "--recipient", dest="sms_recipients", action="append", metavar="PHONE-NUM", help="Cell phone number of message recipient. Can be used multiple times.")
optparser.add_option("-m", "--message", dest="message", action="store", metavar="MESSAGE", help="Message to send to given Recipient(s)")

(options, args) = optparser.parse_args()

## Some mucking with logging levels to enable
## debugging/verbose output for config file parser on request
logging.basicConfig(level=options.verbosity, format='%(levelname)s: %(message)s')

## Now finally parse the config file
try:
	cfg = Config(options.config)
except IOError, e:
	if options.config != default_config_file:
		error("%s: %s"	% (options.config, e.strerror))
		sys.exit(1)
	else:
		cfg = Config()

## And again some logging level adjustments
## according to configfile and command line parameters
if options.verbosity != default_verbosity:
	cfg.verbosity = options.verbosity
logging.root.setLevel(cfg.verbosity)

## Update Config with other parameters
for option in cfg.option_list():
	try:
		if getattr(options, option) != None:
			debug("Updating %s -> %s" % (option, getattr(options, option)))
			cfg.update_option(option, getattr(options, option))
	except AttributeError:
		## Some Config() options are not settable from command line
		pass

if options.dump_config:
	cfg.dump_config(sys.stdout)
	sys.exit(0)

if not options.message or not cfg.sms_recipients:
	sys.stderr.write('Message and at least one recipient must be set!\n')
	sys.exit(1)

sms = SmsSender(cfg.sms_recipients)
sms.send(options.message)
