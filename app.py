import csv
from urllib.parse import urljoin
from flask import json
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

class Basic_Arguments:
    def __init__(self):
        pass

    def get_dates_and_output_file(self):
        today = datetime.datetime.now()
        last_month = today+ relativedelta(months=-1)
        #calculating number of days in previous month
        days_of_previous_month = (date(today.year,today.month, 1) - date(last_month.year, last_month.month, 1)).days
        date_dictionary = {
            'year':str(last_month.year),
            'month':str(last_month.month)
        }
        if int(last_month.month) < 10:
            date_dictionary['month'] = '0' + str(last_month.month)
        startdate = date_dictionary['year'] + date_dictionary['month'] + '01'
        enddate = date_dictionary['year'] + date_dictionary['month'] + str(days_of_previous_month)
        output_dic={
            'year':str(today.year),
            'month':str(today.month),
            'day':str(today.day)
        }
        if int(output_dic['month']) < 10:
            output_dic['month'] = '0' + (output_dic['month'])
        if int(output_dic['day']) < 10:
            output_dic['day'] = '0' + (output_dic['day'])
        csv_filename = 'output_' + output_dic['year'] + output_dic['month'] + output_dic['day'] +'.csv'
        print(csv_filename)
        date_list_output = [csv_filename, startdate, enddate]
        return date_list_output


class Api_connector:
    def __init__(self, autorizathion_request, domains, baseurl):
        self.autorizathion_request = autorizathion_request
        self.domains = domains
        self.baseurl = baseurl
    

    def Akamai_init_report(self):
        foo = Basic_Arguments()
        new_list = foo.get_dates_and_output_file()

        with open(new_list[0], 'w', newline='') as f:
            to_csv_file = csv.writer(f)
            to_csv_file.writerow(['DOMAIN','ALL DNS HITS','NXDOMAIN HITS','STARTDATE','ENDDATE'])
            for line in self.domains:
                domain = str(line.strip('\n'))
                try:
                    result = self.autorizathion_request.get(urljoin(self.baseurl, '/data-dns/v1/traffic/' + domain +'?start=' + new_list[1] + '&start_time=00:00&end=' + new_list[2] +'&end_time=23:59'))
                    some_text = str(result.text)
                    computer_list = []
                    computer_list.append(some_text)
                    computer_list = [w.replace('\n', ',') for w in computer_list] #List Comprehensions
                    outcome = computer_list[0].split(',')
                    for i in range(5):
                        outcome.pop(0)
                    count_dns = 0
                    nx_count = 0
                    for hit in outcome[::3]:
                        count_dns += int(hit)
                    for hit in outcome[1::3]:
                        nx_count += int(hit)
                    to_csv_file.writerow([domain,count_dns,nx_count,new_list[1],new_list[2]])
                    print(domain,',',count_dns,',', nx_count,',', new_list[1], ',',new_list[2])
                except:
                    to_csv_file.writerow([domain,'N/A','N/A',new_list[1],new_list[2]])
                    print(domain,',', 'N/A,','N/A,', new_list[1], new_list[2])
                    
class zone_info_class:
    def __init__(self, autorizathion, zones, baseurl):
        self.autorizathion = autorizathion
        self.zones = zones
        self.baseurl = baseurl

    def get_zone_info(self):
        output_file = 'zone_information.csv'
        with open(output_file, 'w', newline='') as outfile:
            file_to_write = csv.writer(outfile) 
            file_to_write.writerow(['Zone information from Zone records. MX RECORDS, NAMESERVERS & CNAMES'])
            for zone in self.zones:
                try:
                    result = self.autorizathion.get(urljoin(self.baseurl, '/config-dns/v1/zones/' + zone))
                    stringar = result.text
                    if result.status_code == 200:
                        print('\n\n----- Zone Successfully Found For: {} -----'.format(zone.upper()))
                        file_to_write.writerow([])
                        file_to_write.writerow(["----- Zone Successfully Found For: " + zone.upper() + " ------"])
                        document = json.loads(stringar)
                        print('\nMX RECORDS For {}:'.format(zone.upper()))
                        file_to_write.writerow(['MX RECORDS For ' + zone.upper() + ':'])
                        for item in document['zone']['mx']:
                            print('Active: {}, Name: {}, Priority: {}, Target: {}, TTL: {}'.format(item['active'],item['name'],item['priority'],item['target'],item['ttl'], ))
                            file_to_write.writerow(['ACTIVE NAME PRIORITY TARGET TTL', item['active'],item['name'],item['priority'], item['target'],item['ttl']])
                        print('\nNAMESERVERS For {}:'.format(zone.upper()))
                        file_to_write.writerow(['NAMESERVERS For ' + zone.upper() + ':'])
                        for server in document['zone']['ns']:
                            print('Active: {}, Name: {}, Target: {}, TTL: {}'.format(server['active'], server['name'],server['target'], server['ttl']))
                            file_to_write.writerow(['ACTIVE NAME TARGET TTL', server['active'], server['name'], server['target'], server['ttl']])
                        print('\nCNAMES For {}:'.format(zone.upper()))
                        file_to_write.writerow(['CNAMES For ' + zone.upper() + ':'])
                        for name in document['zone']['cname']:
                            print('Active: {}, Name: {}, Target: {}, TTL: {}'.format(name['active'], name['name'], name['target'], name['ttl']))
                            file_to_write.writerow(['ACTIVE NAME TARGET TTL',name['active'],name['name'],name['target'],name['ttl']])
                    else:
                        print(' \n\n----- Unable to find record on: {} -----'.format(zone.upper()))
                        file_to_write.writerow([])
                        file_to_write.writerow(["----- Unable to find record on: " + zone.upper() + " ------"])

                except:
                    print(' \n\n----- Unable to find record on: {} -----'.format(zone.upper()))
                    file_to_write.writerow([])
                    file_to_write.writerow(["----- Unable to find record on: " + zone.upper() + " ------"])
