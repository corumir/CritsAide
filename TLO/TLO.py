#Top Level Object (TLO) information
import os
import re
import json
import crits_API
import crits_DB

config_file = 'TLO/config.json'

#load config.json as config
f_path = os.path.realpath(config_file)
with open(f_path) as json_file:  
    config = json.load(json_file)
json_file.close()

#API variables
api_url = 'http://'+config['IP']+':8080/api/v1/'
api_key = str(config['API_access']['API_Key'])
username = str(config['API_access']['username'])
verify = config['API_access']['verify']

#Database variables
mongo_host = config['IP']
mongo_port = config['DB_access']['mongo_port']
mongo_user = config['DB_access']['mongo_user']
mongo_pass = config['DB_access']['mongo_pass']
db_name = config['DB_access']['db_name']

DB = crits_DB.crits_DB(mongo_host, mongo_port, mongo_user, mongo_pass, db_name)
DB.connect()

class TLO():
	
	@staticmethod
	def typ2cat(typ):
		cat = [x['category'] for x in config['TLO'] if x['TLO_name'] == typ]
		if len(cat) == 1:
			return cat[0]
		else:
			raise KeyError

	@staticmethod
	def get_TLO(typ):
		TLO_return = [config['TLO'][x] for x in range(0,len(config['TLO'])) if config['TLO'][x]['TLO_name'] == typ]
		return TLO_return[0]

	@staticmethod
	def get_attr(TLO_dict, attr):
		attr_return = [TLO_dict['attributes'][x] for x in range(0, len(TLO_dict['attributes'])) if TLO_dict['attributes'][x]['name'] == attr]
		return attr_return[0]

	@staticmethod
	def DB_refresh():
		#update campaign list in config
		config['campaigns'] = [campaign['name'] for campaign in DB.find('campaigns', {})]

		sources = [source['name'] for source in DB.find('source_access', {})]
		for i in range(len(config['TLO'])):
			for j in range(len(config['TLO'][i]['attributes'])):
				if config['TLO'][i]['attributes'][j]['name'] == 'source':
					config['TLO'][i]['attributes'][j]['options'] = sources
					config['TLO'][i]['attributes'][j]['default'] = sources[0]

	@staticmethod
	def add_TLO(typ):
		add_typ = TLO.get_TLO(typ)
		attr_req = []
		attr_req_def = []
		attr_nreq = []
		
		#get attributes for user specified TLO
		for attr in add_typ['attributes']:
			if (attr['required'] == True) and (attr['default'] == None):
				attr_req.append(attr['name'])
			elif (attr['required'] == True) and (attr['default'] != None):
				attr_req_def.append(attr['name'])
			elif attr['required'] == False:
				attr_nreq.append(attr['name'])
		print '\033[96m%s\033[0m ' % ' '.join(attr_req)+'\033[92m%s\033[0m ' % ' '.join(attr_req_def)+' '.join(attr_nreq)
		string = raw_input('Enter Fields (ex. title=TITLE, source=CDI, etc):\n>> ')

		#parse user input
		comma = re.compile("^\s+|\s*,\s*|\s+$") #parse user input by comma and whitespace
		equals = re.compile("\s*=\s*")
		data = {}
		elems = [x for x in comma.split(string) if x]
		for elem in elems:
			pair = [x for x in equals.split(elem) if x]
			data[pair[0]] = pair[1]
		
		#handle CAPS problems
		for key, value in data.iteritems():
			d = TLO.get_attr(add_typ, key)
			if d['default'] != None:
				opt_check = [x for x in d['options'] if x.lower() == value.lower()]
				if len(opt_check) > 0:
					data[key] = opt_check[0]

		#insert defaults for attributes not entered
		for attr in attr_req_def:
			if not (attr in data):
				data[attr] = TLO.get_attr(add_typ, attr)['default']

		API_session = crits_API.crits_API(api_url, api_key, username, verify)
		if ('upload_type' in data) and data['upload_type'] == 'file':
			filepath = raw_input('Enter filepath:\n>> ')
			upload = API_session.upload_file(data, filepath)

		else:
			if ('upload_type' in data) and data['upload_type'] == 'metadata':
				data['data'] = raw_input('Enter data:\n>> ')
			upload = API_session.upload(data, TLO.typ2cat(typ))
		return upload

	approved = [x['TLO_name'] for x in config['TLO']]

	def __init__(self, _type, _name):
		self.type = _type.lower()
		if not self.type in self.approved:
			raise ValueError
		self.name = _name
		self.call = self.get_TLO(self.type)['attributes'][0]['name']
		self.collection = self.typ2cat(self.type)

	def get(self):
		return DB.find_one(self.collection, {self.call:self.name})
	
	def get_ID(self):
		doc = self.get()
		return doc['_id']

	def delete(self):
		return DB.delete_one(self.collection, {self.call:self.name})

	def relationship(self, Right_TLO):
		if 'relationships' in self.get():
			for relationship in self.get()['relationships']:
				if relationship['value'] == Right_TLO.get_ID():
					return False

		API_session = crits_API.crits_API(api_url, api_key, username, verify)
		result = API_session.build_relationship(self, Right_TLO)
		return result

	def add_campaign(self, new_campaign):
		campaign_exist = False
		for campaign in config['campaigns']:
			if new_campaign.lower() == campaign.lower():
				new_campaign = campaign
				campaign_exist = True

		if campaign_exist:
			result = DB.add_campaign(self, new_campaign, username)
			return result
		else:
			return False
		