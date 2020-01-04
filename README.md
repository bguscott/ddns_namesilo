# ddns_namesilo
Automated NameSilo DNS A record update with current IP. Run on a machine on your network and it will auto-update NameSilo DNS records and subdomains with your current IP. If a subdomain is provided that doesn't exist, it's created in the process.

Just update the script with your NameSilo API key, desired domain or subdomain names, and run the script using cron.

## Requirements
* Python 2.7
* Python "requests" module installed. E.g.,:
    * `python2.7 -m ensurepip`
    * `python2.7 -m pip install requests`
    * `python2.7 -m pip install –-upgrade pip`
* xml module

## Installation
1. Copy the python script "ddns_namesilo_update.py" to your system
2. Edit ddns_namesilo_update.py and change the variables ot suit your environment:
    * `API_KEY` - (from NameSilo account page)
    * `DOMAIN` - domain name (e.g., `"example.com"`)
    * `SUB_DOMAIN` - sub domains of `DOMAIN` in list format (e.g., `["wiki","mail"]`)
3. Create a cron job to run the script, being mindful of API limits of the provider. E.g.,:

    ```*/5 * * * * root /usr/local/bin/python2.7 <path to file>/ddns_namesilo_update.py | /usr/bin/logger -t ddns_namesilo_update```
