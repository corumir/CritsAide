import datetime
import pymongo

class crits_DB():
    def __init__(self, mongo_host, mongo_port, mongo_user, mongo_pass, db_name):
       
        auth_str = ''
        if mongo_user != '':
            auth_str = mongo_user
        if mongo_pass != '' and mongo_user != '':
            auth_str = auth_str + ':' + mongo_pass
        if auth_str != '':
            auth_str = auth_str + '@'
        
        # Build the URI
        self.mongo_uri = 'mongodb://{}{}:{}'.format(auth_str, mongo_host, mongo_port)
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]

    def find(self, collection, query):
        obj = getattr(self.db, collection)
        result = obj.find(query)
        return result

    def find_one(self, collection, query):
        obj = getattr(self.db, collection)
        result = obj.find_one(query)
        return result

    def delete_one(self, collection, query):
        obj = getattr(self.db, collection)
        result = obj.delete_one(query)
        return result

    def add_campaign(self, TLO, campaign, analyst):
        obj = getattr(self.db, TLO.collection)
        result = obj.find({'_id': TLO.get_ID(), 'campaign.name': campaign})
        if result.count() > 0:
            return None
        else:
            campaign_obj = {
                'analyst': analyst,
                'confidence': 'medium',
                'date': datetime.datetime.now(),
                'description': '',
                'name': campaign
            }
            result = obj.update(
                {'_id': TLO.get_ID()},
                {'$push': {'campaign': campaign_obj}}
            )
            return result