import csv
from urllib.parse import urljoin
from flask import json


class Api_connector:
    def __init__(self, autorizathion_request, time_list, domains, baseurl):
        self.autorizathion_request = autorizathion_request
        self.time_list = time_list
        self.domains = domains
        self.baseurl = baseurl

    def Akamai_init_report(self):
        with open(self.time_list[0], 'w', newline='') as f:
            to_csv_file = csv.writer(f)
            to_csv_file.writerow(['DOMAIN','ALL DNS HITS','NXDOMAIN HITS','STARTDATE','ENDDATE'])
            for line in self.domains:
                domain = str(line.strip('\n'))
                try:
                    result = self.autorizathion_request.get(urljoin(self.baseurl, '/data-dns/v1/traffic/' + domain +'?start=' + self.time_list[1] + '&start_time=00:00&end=' + self.time_list[2] +'&end_time=23:59'))
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
                    to_csv_file.writerow([domain,count_dns,nx_count,self.time_list[1],self.time_list[2]])
                    print(domain,',',count_dns,',', nx_count,',', self.time_list[1], ',',self.time_list[2])
                except:
                    to_csv_file.writerow([domain,'N/A','N/A',self.time_list[1],self.time_list[2]])
                    print(domain,',', 'N/A,','N/A,', self.time_list[1], self.time_list[2])
                    
class zone_info_class:
    def __init__(self, autorizathion, zones, baseurl):
        self.autorizathion = autorizathion
        self.zones = zones
        self.baseurl = baseurl

    def get_zone_info(self):
        for zone in self.zones:
            try:
                result = self.autorizathion.get(urljoin(self.baseurl, '/config-dns/v1/zones/' + zone))
                stringar = result.text

                document = json.loads(stringar)
                print('\n', document['zone']['name'], '\n')
                for item in document['zone']['ns']:
                    print(item['target'])
            except:
                print('error')
