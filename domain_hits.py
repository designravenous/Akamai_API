import datetime
import config
import app

file_argument = 'test.txt'

with open(file_argument, 'r') as input_file:
    domains = input_file.readlines()
input_file.close()

current_date = datetime.datetime.now()

#get credentials from Config.py:
to_akamai = config.Akamai_credentials(current_date)
s = to_akamai.Akamai_report()


#Calling on API Connector:
api_call = app.Api_connector(s[0], domains, s[1])
#Calling method creating Report:
api_call.Akamai_init_report()
