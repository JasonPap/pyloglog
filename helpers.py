#!/usr/bin/python

import os
from datetime import datetime , timedelta
from failed_login_record import failed_login_record

def process_data(rec, failed_attempts, valid_username):
        attr = rec.split()
        time = datetime.strptime(str(datetime.now().year) + " " + attr[0] + " " + attr[1] + " " + attr[2],'%Y %b %d %H:%M:%S')
        username = None
        ip = None
        if valid_username:
                username = attr[8]
                ip = attr[10]
        else:
                username = attr[10]
                ip = attr[12]
        record = failed_login_record(ip, time, username)
	
	return record


def usage():
	print "\t -h, --help to see usage manual."
	print "\t -o=<filename> or --output=<filename> to set the output filename."
	print "\t -l, --localize to enable geo-location of each failed login record"


def get_configurations():
	configs = dict()
	CONFPATH = "./config.txt"
	if os.path.isfile(CONFPATH) and not os.access(CONFPATH, os.R_OK):
		print "config.txt is not readable"
        	sys.exit(3)
	else:
        	with open(CONFPATH,'a+') as config_file:
                	config_file.seek(0)
                	for line in config_file:
				print "DEBUG:"+line.rstrip()+"."
                        	param = line.rstrip().split(" ", 2)
                        	if param[0] == "fromdate":
                                	configs[param[0]] = datetime.strptime(param[1],'%Y/%m/%d_%H:%M:%S')
                        	else:
					configs[param[0]] = param[1]

                	if "fromdate" not in configs:
                        	fromdate = datetime.now() - timedelta(days=7)
                        	configs["fromdate"] = fromdate
                	if "OSlogfile" not in configs:
                        	configs["OSlogfile"] = "/var/log/auth.log"      # default location of authentication logs
                	if "outputSeparator" not in configs:
                        	configs["outputSeparator"] = ","
	
	return configs

def store_configuration(configs):
	CONFPATH="./config.txt"
	with open(CONFPATH,"w") as config_file:
		cnf_txt = ""
		for attr in configs:
			key = attr
			val = configs[key]
			if key == "fromdate":
				cnf_txt += key + " " + datetime.strftime(val, '%Y/%m/%d_%H:%M:%S') + "\n"
			else:
				cnf_txt += key + " " + val + "\n"
		config_file.write(cnf_txt)
