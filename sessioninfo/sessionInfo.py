from botScore.mongoQuery import Mongo
import datetime


class sessionInfo():
    def __init__(self,host,db,collection,refNum="PHENA0059"):
        mongo=Mongo(host)
        mongo.get_db(db, collection)
        self.mongo=mongo
        self.refNum=refNum
    def getSessionId(self,from_dt=None,to_dt=None):
        complete_data=self.mongo.query_db(self.get_query(from_dt,to_dt),projection={"user_details.ptSessionId"})
        return [{"id" : data["user_details"]["ptSessionId"]} for data in complete_data  if "user_details" in data]

    def getConversations(self,session_id=None,from_dt=None,to_dt=None):
        complete_data=self.mongo.query_db({"user_details.botResponse.messages"},self.get_query(from_dt,to_dt,session_id))
        return [data["user_details"]["botResponse"]["messages"] for data in complete_data]


    def get_query(self,from_dt,to_dt,session_id=None):
        query=[]
        if(from_dt!=None):
            query.append({"timeStamp":{"$gt" : datetime.datetime.strptime(from_dt,'%Y-%m-%d')}})
        if(to_dt != None):
            query.append({"timeStamp":{"$lt" : datetime.datetime.strptime(to_dt,'%Y-%m-%d')}})
        if(session_id!=None):
            query.append({"user_details.ptSessionId" : session_id})
        if(len(query)==0):
            return {}
        return {"$and" : query}

if __name__ == "__main__":
    host="mongodb://pheglodev:goodDevelopers%401@dev-ng-mongo1.phenompeople.com:27017,dev-ng-mongo2.phenompeople.com:27017,dev-ng-mongo3.phenompeople.com:27017/mongo_ngcc_dev?readPreference=primary"
    db="mongo_chatbot"
    collection="USER_CONVERSATIONS"
    sessionInfo(host,db,collection).getSessionId()
    sessionInfo(host,db,collection).getConversations("1")

