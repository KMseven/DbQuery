import datetime

from constants.Constants import Collections
from src.botScore.mongoQuery import Mongo
from src.config import get_db_name, get_db_url


class leadgen():

    def __init__(self,mongo):
        self.mongo=mongo

    def get_score(self,from_dt=None,to_dt=None,refNum=None):

        no_of_leads_generated=self.mongo.query_db(self.generate_query(from_dt,to_dt,refNum,True),True)

        no_of_leads_attempted=self.mongo.query_db(self.generate_query(from_dt,to_dt,refNum,False),True)
        return no_of_leads_generated/no_of_leads_attempted

    def generate_query(self,from_dt,to_dt,refNum,is_generated=False):
        if(is_generated):
            query={"userDetails.userName": {"$exists": True}, "userDetails.userContact": {"$exists": True},
                       "userDetails.userSkills": {"$exists": True}, "userDetails.userLocations": {"$exists": True},
                       "userDetails.userJobTitle": {"$exists": True}, "userDetails.userCompanyName": {"$exists": True}}
        else:
            query={}
        if(from_dt!=None):
            query["timeStamp"] = { "$gte": datetime.datetime.strptime(from_dt, '%Y-%m-%d')}
        if(to_dt!=None):
            query["timeStamp"] = { "$lt": datetime.datetime.strptime(to_dt, '%Y-%m-%d')}
        if(refNum!=None):
            query["refNum"]=refNum
        return query


if __name__ =="__main__":
    host =get_db_url()
    db = get_db_name()
    collection = Collections.USERS
    mongo = Mongo(host)
    mongo.get_db(db, collection)
    print("F:",leadgen(mongo).get_score("PHENA0059"))