#!/usr/bin/python

from geo_ip import *
from datetime import datetime

class failed_login_record:
	def __init__(self, ip, time, username):
		self.ip = ip
		self.time = time
		self.username = username
		self.country = None
		self.latitude = None
		self.longitude = None
	
	def geo_locate(self):
		if self.latitude is not None:	# this record has already
			return			# been geo-located
		
		results = get_geolocation_for_ip(self.ip)
		self.country = results["country_name"]
		self.latitude = results["latitude"]
		self.longitude = results["longitude"]
		return		
	
	def to_string(self, separator):
	# can be done with .join string method for greater speed
		retval = self.time.strftime("%Y/%m/%d_%H:%M:%S")
		retval += separator + self.ip
		retval += separator + self.username
		if self.latitude != None:
			retval += separator + str(self.latitude)
		if self.longitude != None:
                        retval += separator + str(self.longitude)
		if self.country != None:
                        retval += separator + self.country
		return retval

def localize_records(l_records):
	geo_ip_cache = dict()	#key: string with IP,	value: tuple (country, lat, lon)
	bad_records = []
	for record in l_records:
		if record.ip not in geo_ip_cache:
			try:
				record.geo_locate()
				geo_ip_cache[record.ip] = (record.country, record.latitude, record.longitude)
			except requests.exceptions.HTTPError:
				print "DEBUG: record not inserted = " + record.to_string(",")
				bad_records.append(record)
		else:
			record.country = geo_ip_cache[record.ip][0]
			record.latitude = geo_ip_cache[record.ip][1]
			record.longitude = geo_ip_cache[record.ip][2]
	
	l_records[:] = [record for record in l_records if record not in bad_records]
