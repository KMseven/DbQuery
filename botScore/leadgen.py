import datetime

from botScore.mongoQuery import Mongo


class leadgen():

    def __init__(self,host,db,collection):
        mongo=Mongo(host)
        mongo.get_db(db, collection)
        self.mongo=mongo

    def get_score(self):
        from_dt=datetime.datetime.strptime('2018-09-06', '%Y-%m-%d')
        no_of_leads_generated=self.mongo.query_db({"userDetails.userName": {"$exists": True}, "userDetails.userContact": {"$exists": True},
                       "userDetails.userSkills": {"$exists": True}, "userDetails.userLocations": {"$exists": True},
                       "userDetails.userJobTitle": {"$exists": True}, "userDetails.userCompanyName": {"$exists": True},
                        "timeStamp": { "$gte": from_dt}},True)

        no_of_leads_attempted=self.mongo.query_db({"timeStamp": { "$gte": from_dt}},True)
        return no_of_leads_generated/no_of_leads_attempted



if __name__ =="__main__":
    host="mongodb://esuser:D5l09tt5%24l95n%21@deloitteg-db1.imomentous.co:27017,deloitteg-db2.imomentous.co:27017,deloitteg-db3.imomentous.co:27017/admin?readPreference=primary"
    db="mongo_chatbot"
    collection="users"
    print("F:",leadgen(host,db,collection).get_score())