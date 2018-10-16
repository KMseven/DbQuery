import datetime

from constants.Constants import Constants, Collections
from src.botScore.mongoQuery import Mongo
from src.config import get_db_url, get_db_name


class UnknownIntent():

    def __init__(self,mongo):
        self.mongo=mongo

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
            query.append({Constants.TIMESTAMP:{"$gt" : datetime.datetime.strptime(from_dt,Constants.DATE_FORMAT)}})
        if(to_dt != None):
            query.append({Constants.TIMESTAMP:{"$lt" : datetime.datetime.strptime(to_dt,Constants.DATE_FORMAT)}})
        if(refNum!=None):
            query.append({Constants.USER_DETAILS+"."+Constants.REFNUM: refNum})
        if(get_uid):
            query.append({Constants.USER_DETAILS+"."+Constants.BOT_ACTION : Constants.UTTER_UNINTERPRETABLE})
        else:
            if (session_id != None):
                query.append({Constants.USER_DETAILS+"."+Constants.PTSESSIONID: session_id})

        if(len(query)==0):
            return {}
        return {"$and" : query}

if __name__==  "__main__":
    host =get_db_url()
    db = get_db_name()
    collection = Collections.USER_CONVERSATIONS
    mongo = Mongo(host)
    mongo.get_db(db, collection)
    obj = UnknownIntent(mongo);
    array = obj.getUidForUnknownIntent()
    i = 0;
    while i < len(array) :
        print("id...",array[i])
        arrayObj = obj.getDocForUid(array[i]['user_details']['ptSessionId'])
        print("result = ",arrayObj)
        i += 1
    print("caller  ends")
