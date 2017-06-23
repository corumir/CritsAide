import json
import requests
import datetime

class crits_API():

    def __init__(self, api_url='', api_key='', username='', verify=True):
        self.url = api_url
        if self.url[-1] == '/':
            self.url = self.url[:-1]
        self.api_key = api_key
        self.username = username
        self.verify = verify

    def upload(self, data, category):
        
        data['username'] = self.username
        data['api_key'] = self.api_key

        r = requests.post("%s/%s/" % (self.url, category), data=data, verify=self.verify)

        if r.status_code == 200:
            JSON = json.loads(r.text)
            return JSON

        return None

    def upload_file(self, data, filepath, category):
        data['username'] = self.username
        data['api_key'] = self.api_key
        
        with open(filepath, 'rb') as fdata:
            r = requests.post('%s/%s/'%(self.url, category), 
                    data=data, 
                    files={'filedata': fdata}, 
                    verify=self.verify)
            if r.status_code == 200:
                result_data = json.loads(r.text)
                return result_data
            else:
                return {'message':'upload unsuccessful'}

    def build_relationship(self, Left_TLO, Right_TLO):
        right_type = Right_TLO.type[:1].upper() + Right_TLO.type[1:] #handles CAPS issue
        submit_url = '{}/{}/{}/'.format(self.url, Left_TLO.collection, Left_TLO.get_ID())

        params = {'api_key': self.api_key,'username': self.username}
        data = {
            'action': 'forge_relationship',
            'type_': Left_TLO.type,
            'id_': Left_TLO.get_ID(),
            'right_type': right_type,
            'right_id': Right_TLO.get_ID(),
            'rel_type': 'Related To',
            'rel_date': datetime.datetime.now(),
            'rel_reason': '',
            'rel_confidence': 'low',
            'get_rels': True
        }

        r = requests.patch(submit_url, params=params, data=data, verify=False)
        if r.status_code == 200:
            return json.loads(r.text)
        else:
            return None