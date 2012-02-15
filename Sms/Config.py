## Author: Michal Ludvig <michal@logix.cz>
##         http://www.logix.cz/michal
## License: GPL Version 2

import logging
from logging import debug, info, warning, error
import re

from Exceptions import *

class Config(object):
	_instance = None
	_parsed_files = []

	sms_engine = "GwGenericHttp"	## Module must contain class SmsDriver
	sms_recipients = [ ]
	sms_url_pattern = ""
	sms_message = ""
	sms_timestamp_format = "%m/%d %H:%M"
	## Example config for Clickatell:
	## sms_engine = "GwClickatell"
	## sms_url_pattern = "https://api.clickatell.com/http/sendmsg?api_id=APIID&user=USERNAME&password=PASSWORD&to=%(recipient)s&text=%(message)s"
	## replace APIID, USERNAME and PASSWORD with the values of your Clickatell account

	profile = "default"
	verbosity = logging.INFO

	## Creating a singleton
	def __new__(self, configfile = None, profile = None):
		if self._instance is None:
			self._instance = object.__new__(self)
		return self._instance

	def __init__(self, configfile = None, profile = None):
		if profile:
			self.profile = profile
		if configfile:
			self.read_config_file(configfile)

	def option_list(self):
		retval = []
		for option in dir(self):
			## Skip attributes that start with underscore or are not string, int or bool
			option_type = type(getattr(Config, option))
			if option.startswith("_") or \
			   not (option_type in (
			   		type("string"),	# str
			        	type(42),	# int
					type(True),	# bool
					type([]))):	# list
				continue
			retval.append(option)
		return retval

	def read_config_file(self, configfile):
		cp = ConfigParser(configfile, self.profile)
		for option in self.option_list():
			self.update_option(option, cp.get(option))
		self._parsed_files.append(configfile)

	def update_option(self, option, value):
		if value is None:
			return
		#### Special treatment of some options
		## verbosity must be known to "logging" module
		if option == "verbosity":
			try:
				setattr(Config, "verbosity", logging._levelNames[value])
			except KeyError:
				error("Config: verbosity level '%s' is not valid" % value)
		## allow yes/no, true/false, on/off and 1/0 for boolean options
		elif type(getattr(Config, option)) is type(True):	# bool
			if str(value).lower() in ("true", "yes", "on", "1"):
				setattr(Config, option, True)
			elif str(value).lower() in ("false", "no", "off", "0"):
				setattr(Config, option, False)
			else:
				error("Config: value of option '%s' must be Yes or No, not '%s'" % (option, value))
		elif type(getattr(Config, option)) is type(42):		# int
			try:
				setattr(Config, option, int(value))
			except ValueError, e:
				error("Config: value of option '%s' must be an integer, not '%s'" % (option, value))
		else:							# string
			setattr(Config, option, value)

class ConfigParser(object):
	def __init__(self, cfgfile, section):
		self.cfg = {}
		self.parse_file(cfgfile, section)
	
	def parse_file(self, cfgfile, section):
		debug("ConfigParser: Reading file '%s' [section: %s]" % (cfgfile, section))
		in_our_section = False
		our_section_found = False
		try:
			f = open(cfgfile, "r")
		except Exception, e:
			error(str(e))
			raise
		r_comment = re.compile("^\s*#.*")
		r_empty = re.compile("^\s*$")
		r_section = re.compile("^\[([^\]]+)\]")
		r_data = re.compile("^\s*(?P<key>\w+)\s*=\s*(?P<value>.*)")
		r_quotes = re.compile("^\"(.*)\"\s*$")
		for line in f:
			line = line.strip()
			if r_comment.match(line) or r_empty.match(line):
				continue
			is_section = r_section.match(line)
			if is_section:
				this_section = is_section.groups()[0]
				in_our_section = (this_section == section)
				continue
			if not in_our_section:
				continue
			our_section_found = True
			is_data = r_data.match(line)
			if is_data:
				data = is_data.groupdict()
				if r_quotes.match(data["value"]):
					data["value"] = data["value"][1:-1]
				self.__setitem__(data["key"], data["value"])
				if data["key"] in ("db_pass"):
					print_value = "..."
				else:
					print_value = data["value"]
				debug("ConfigParser: %s->%s" % (data["key"], print_value))
				continue
			raise SmsConfigError("%s: invalid line: %s" % (cfgfile, line))
		if not our_section_found:
			raise SmsConfigError("%s: profile [%s] not found" % (cfgfile, section))

	def __getitem__(self, name):
		return self.cfg[name]
	
	def __setitem__(self, name, value):
		self.cfg[name] = value
	
	def get(self, name, default = None):
		if self.cfg.has_key(name):
			return self.cfg[name]
		return default

