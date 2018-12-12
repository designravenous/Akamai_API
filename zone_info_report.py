import config
import app
import datetime

zones = ['pleat.com', 'hm.com', 'afound.com']
date = datetime.datetime.now()
todays_date = str(date.today)

#getting credentials
credentials = config.Akamai_credentials(todays_date)
s = credentials.Akamai_zone_read()

#credentials_list = [s, baseurl]
get_class = app.zone_info_class(s[0],zones, s[1])
get_class.get_zone_info()
