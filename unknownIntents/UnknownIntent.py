import datetime

from botScore.mongoQuery import Mongo

class UnknownIntent():

    def __init__(self,host,db,collection):
        self.host = host
        self.mongo = Mongo(self.host)
        self.collection = self.mongo.get_db(db,collection)


    def getUidForUnknownIntent(self,from_dt=None,to_dt=None,refNum="PHENA0059"):
        docs=self.mongo.query_db(self.generate_query(from_dt,to_dt,True,refNum),projection={"user_details.ptSessionId":1, "_id":0})
        array = list(docs)
        return array

    def getDocForUid(self,session_id,from_dt=None,to_dt=None,refNum="PHENA0059"):
        docs=self.mongo.query_db(self.generate_query(from_dt,to_dt,session_id=session_id,refNum=refNum),projection={"user_details.request":1,"user_details.botResponse.messages":1,"_id":0})
        array = list(docs)
        return array

    def generate_query(self,from_dt,to_dt,get_uid=False,session_id=None,refNum="PHENA0059"):
        query=[]
        if(from_dt!=None):
            query.append({"timeStamp":{"$gt" : datetime.datetime.strptime(from_dt,'%Y-%m-%d')}})
        if(to_dt != None):
            query.append({"timeStamp":{"$lt" : datetime.datetime.strptime(to_dt,'%Y-%m-%d')}})
        if(refNum!=None):
            query.append({"user_details.refNum": refNum})
        if(get_uid):
            query.append({"user_details.botAction": "UTTER_UNINTERPRETABLE"})
        else:
            if (session_id != None):
                query.append({"user_details.ptSessionId": session_id})

        if(len(query)==0):
            return {}
        return {"$and" : query}

if __name__==  "__main__":
    host="mongodb://pheglodev:goodDevelopers%401@dev-ng-mongo1.phenompeople.com:27017,dev-ng-mongo2.phenompeople.com:27017,dev-ng-mongo3.phenompeople.com:27017/mongo_ngcc_dev?readPreference=primary"
    db="mongo_chatbot"
    collection="USER_CONVERSATIONS"
    obj = UnknownIntent(host,db,collection);
    array = obj.getUidForUnknownIntent()
    i = 0;
    while i < len(array) :
        print("id...",array[i])
        arrayObj = obj.getDocForUid(array[i]['user_details']['ptSessionId'])
        print("result = ",arrayObj)
        i += 1
    print("caller  ends")
