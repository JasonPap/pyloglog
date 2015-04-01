#!/usr/bin/python

import os
import os.path
import sys
import getopt
from helpers import *
from datetime import datetime
from failed_login_record import localize_records

def main():
	# Initialization #

	# Parsing of arguments #
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ho:l", ["help", "output=","localize"])
	except getopt.GetoptError as err:
	# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	output = "defaultlog.csv"
	localize = False
	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-o", "--output"):
			output = a
		elif o in ("-l", "--localize"):
			localize = True
		else:
			assert False, "unhandled option"

	# Reading of configuration file #
	configs = get_configurations()

	# Reading of OS logfile #	
	raw_failed_attempts = []
	with open(configs["OSlogfile"]) as system_log:
		for line in system_log:
			if "Failed" in line:
				raw_failed_attempts.append(line)


	# Formating of records #
	failed_attempts = []
	for attempt in raw_failed_attempts:
		record = None
		if "invalid" in attempt:
			record = process_data(attempt, failed_attempts, False)
		else:
			record = process_data(attempt, failed_attempts, True)
		
		# Remove everything before the fromdate (from config) #
		if record.time > configs["fromdate"]:
			failed_attempts.append(record)	
	
	#localize reocrds if -l argument was given
	if localize:
		localize_records(failed_attempts)
	
	# get time of last record processed
	if failed_attempts:
		configs["fromdate"] = failed_attempts[-1].time
	else:
		print "No records were found from the 'fromdate' to now"
		return

	# Write output #
	separator = configs["outputSeparator"]
	with open(output,'a+') as outfile:
		outtext = ""
		for record in failed_attempts:
			outtext += record.to_string(separator) + "\n"
		outfile.write(outtext)
	
	# Write config file #
	store_configuration(configs)
	print "exiting"

if __name__ == "__main__":
	main()
