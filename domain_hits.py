import sys
import datetime
import config
import app

def check_for_argument():
    print('--- Error ---')
    print('--- Script should contain 3 arguments ---')
    print('--- File type txt each domain devided by line---')
    print('--- Startdate, example 20190101 ---')
    print('--- Enddate, example 20190131 ---')
    exit()

try:
    file_argument = sys.argv[1]
    starting = sys.argv[2]
    ending = sys.argv[3]
except:
    check_for_argument()

with open(file_argument, 'r') as input_file:
    domains = input_file.readlines()
input_file.close()

current_date = datetime.datetime.now()

#get credentials from Config.py:
to_akamai = config.Akamai_credentials(current_date)
s = to_akamai.Akamai_report()

csv_filename = 'output_' + str(current_date.year)+str(current_date.month) + str(current_date.day) + '.csv'
start_date = str(starting)
end_date = str(ending)
time_list = [csv_filename, start_date, end_date]

#Calling on API Connector:
api_call = app.Api_connector(s[0], time_list, domains, s[1])
#Calling method creating Report:
api_call.Akamai_init_report()



