# ddns_namesilo
Automated NameSilo DNS record update with current IP

Just update the script with your NameSilo API key, desired domain or subdomain names, and runt he script using cron:

e.g., cron job that runs every 5 minutes and sends logs to syslog:

```*/5 * * * * root /usr/local/bin/python2.7 <path to file>/ddns_namesilo_update.py | /usr/bin/logger -t ddns_namesilo_update```
