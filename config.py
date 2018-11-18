from akamai.edgegrid import EdgeGridAuth
import requests

class Akamai_credentials:
    def __init__(self, datetime):
        self.datetime = datetime
    def Akamai_report(self):
        s = requests.Session()
        s.auth = EdgeGridAuth(
            client_token='XXXXXXXXXXXXXXXXXXXXXXX',
            client_secret='XXXXXXXXXXXXXXXXXXXXXX',
            access_token='XXXXXXXXXXXXXXXXXXXXXXXXX'
        )
        baseurl = 'https://XXXXXXXXXXXXXXX.luna.akamaiapis.net/'
        credentials_list = [s, baseurl]
        return credentials_list
