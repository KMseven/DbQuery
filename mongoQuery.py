from pymongo import MongoClient
from pymongo.database import Database


class Mongo():
    def __init__(self,host=None,port=None,username=None,password=None):

        self.host=host
        self.port=port
        self.username=username
        self.password=password

    def get_db(self,db,collection):
        mongoClient=MongoClient(self.host)
        self.db=mongoClient[db][collection]
        return db

    def query_db(self,query,get_length=False):
        if(get_length):
            return self.db.find(query).count()
        complete_data=[]
        for data in self.db.find(query):
            complete_data.append(data)
        return complete_data

if __name__ == "__main__":
    mongo=Mongo("mongodb://pheglodev:goodDevelopers%401@dev-ng-mongo1.phenompeople.com:27017,dev-ng-mongo2.phenompeople.com:27017,dev-ng-mongo3.phenompeople.com:27017/mongo_ngcc_dev?readPreference=primary")
    mongo.get_db("mongo_chatbot","users");
    mongo.query_db({ "userDetails.userName": { "$exists": True }, "userDetails.userContact": { "$exists": True }, "userDetails.userSkills": { "$exists": True }, "userDetails.userLocations": { "$exists": True }, "userDetails.userJobTitle": { "$exists": True }, "userDetails.userCompanyName": { "$exists": True } })