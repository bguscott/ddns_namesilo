#!/usr/bin/python
# coding=utf_8
#
# NameSilo DNS Update script 
# Must install requests package first
# python2.7 -m ensurepip
# python2.7 -m pip install requests
# python2.7 -m pip install –-upgrade pip

import requests
import xml.etree.ElementTree as ET

API_KEY= ""
DOMAIN = ""
SUB_DOMAIN = ["", ""]
RECORD_IP_ADDRESS_URL = "https://www.namesilo.com/api/dnsListRecords?version=1&type=xml&key=" + API_KEY + "&domain=" + DOMAIN
CURRENT_IP_ADDRESS_URL = "http://whatismyip.akamai.com/"

#get current IP address from CURRENT_IP_ADDRESS_URL
current = requests.get(CURRENT_IP_ADDRESS_URL).content
print("Current IP address from akamai: %s \n" % current)

#read xml file
r = requests.get(RECORD_IP_ADDRESS_URL, allow_redirects=True)
xml = ET.fromstring(r.content)

#begin parsing xml for correct host (DOMAIN)
for record in xml.iter("resource_record"):
	#read host, value, and record_id from current record in xml
	host = record.find("host").text
	value = record.find("value").text
	record_id = record.find("record_id").text

	# if host is SUB_DOMAIN, process further
	for domain_i in SUB_DOMAIN:
		if (host == domain_i + "." + DOMAIN):
			print("Current " + host + " namesilo record IP address is: %s" % value)
		
			#if record IP address matches CURRENT_IP_ADDRESS_URL, do nothing
			if (value == current):
				print("Current IP address matches namesilo record for %s \n" % host)
				break
				
			#IP addresses don’t match, let’s update it
			else:
				print("IP addresses do not match, generating URL to update")

				#place the record_id in the url
				new_URL = "https://www.namesilo.com/api/dnsUpdateRecord?version=1&type=xml&key=" + API_KEY + "&domain=" + DOMAIN + "&rrid=" + record_id + "&rrhost=" + domain_i + "&rrvalue=" + current + "&rrttl=3600"
				print(new_URL)

				#send request to URL
				new = requests.get(new_URL)

				#print the xml reply, this doesn't need to be pretty
				print(new.content + "\n")
				break
