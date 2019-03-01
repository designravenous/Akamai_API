import config
import app
import datetime


date = datetime.datetime.now()
todays_date = str(date.today)

file_argument = 'DNS_zoner.txt'

with open(file_argument, 'r') as input_file:
    domains = input_file.readlines()
input_file.close()
zones = []
for item in domains:
    new_dom = str(item.strip('\n'))
    zones.append(new_dom)
    

#getting credentials
credentials = config.Akamai_credentials(todays_date)
s = credentials.Akamai_zone_read()

#credentials_list = [s, baseurl]
get_class = app.zone_info_class(s[0],zones, s[1])
get_class.get_zone_info()
