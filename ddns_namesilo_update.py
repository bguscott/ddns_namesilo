#!/usr/bin/python
# coding=utf_8
#
# Description:
# 	NameSilo DNS update with current IP script. Run on a machine on your network and it will auto-update
#	NameSilo DNS records and subdomains with your current IP. If a subdomain is provided that doesn't exist,
#	it's created in the process.
#
#	Works well setup as a script in pfsense (or similar) for remote access to your home network. 
#	Just set up cron (e.g., every 30 minutes) with something similar to:
#		/usr/local/bin/python3.7 /usr/local/ddns_namesilo_update.py | /usr/bin/logger -t ddns_namesilo_update
#
# Must install requests package first and update pip:
# 	python3 -m ensurepip
# 	python3 -m pip install requests
# 	python3 -m pip install --upgrade pip

import requests
import xml.etree.ElementTree as ET

API_KEY= ""		# API key for namesilo
DOMAIN = "" 		# E.g., "yourdomain.com"
SUB_DOMAIN = ["", ""] 	# E.g., "mail" for "mail.yourdomain.com"; You can list multiple sub-domains to update
RECORD_IP_ADDRESS_URL = "https://www.namesilo.com/api/dnsListRecords?version=1&type=xml&key=" + API_KEY + "&domain=" + DOMAIN
CURRENT_IP_ADDRESS_URL = "http://whatismyip.akamai.com/"

#get current IP address from CURRENT_IP_ADDRESS_URL
current_ip = requests.get(CURRENT_IP_ADDRESS_URL).content
print("Current IP address from akamai: %s \n" % current_ip)

#read xml file
r = requests.get(RECORD_IP_ADDRESS_URL, allow_redirects=True)
xml = ET.fromstring(r.content)

#list for updating with new A records
domain_status = dict({status:"unknown" for status in SUB_DOMAIN})

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
			if (value == current_ip):
				print("Current IP address matches namesilo record for %s \n" % host)
				domain_status[domain_i] = "exists"
				break
				
			#IP addresses don’t match, let’s update it
			else:
				print("IP addresses do not match, generating URL to update")
				new_URL = "https://www.namesilo.com/api/dnsUpdateRecord?version=1&type=xml&key=" + API_KEY + "&domain=" + DOMAIN + "&rrid=" + record_id + "&rrhost=" + domain_i + "&rrvalue=" + current_ip + "&rrttl=3600"
				print(new_URL)

				#send request to URL
				new = requests.get(new_URL)

				#print the xml reply
				print(new.content + "\n")
				
				domain_status[domain_i] = "updated"
				break

#case in which a subdomain currently doesn't exist (value in domain_status for a subdomain is "unknown")
for domain_i in domain_status:
	if domain_status[domain_i] == "unknown":
		print("\"A\" record " + domain_i + "." + DOMAIN + " doesn't exist, generating URL for new A record.")
		new_URL = "https://www.namesilo.com/api/dnsAddRecord?version=1&type=xml&key=" + API_KEY + "&domain=" + DOMAIN + "&rrtype=A" + "&rrhost=" + domain_i + "&rrvalue=" + current_ip + "&rrttl=3600"
		print(new_URL + "\n")
		
		#send request to URL
		new = requests.get(new_URL)
		
		#print the xml reply
		print(new.content + "\n")
			
		domain_status[domain_i] = "updated"
		break
