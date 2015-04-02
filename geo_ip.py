import requests

FREEGEOPIP_URL = 'http://freegeoip.net/json/'

SAMPLE_RESPONSE = """{
    "ip":"108.46.131.77",
    "country_code":"US",
    "country_name":"United States",
    "region_code":"NY",
    "region_name":"New York",
    "city":"Brooklyn",
    "zip_code":"11249",
    "time_zone":"America/New_York",
    "latitude":40.645,
    "longitude":-73.945,
    "metro_code":501
}"""


def get_geolocation_for_ip(ip):
	url = '{}/{}'.format(FREEGEOPIP_URL, ip)

	response = requests.get(url)
	try:
		response.raise_for_status()
	except requests.exceptions.HTTPError:
		print "ERROR: url=" + str(url)
		print response.status_code
		raise
	if response.status_code != requests.codes.ok:
		sys.stderr.write("free geo-ip 10k requests/hour limit reached\n")
	return response.json()
