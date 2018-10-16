from constants.Constants import Constants, Collections
from src.botScore.mongoQuery import Mongo
import datetime

from src.config import get_db_url, get_db_name


class sessionInfo():
    def __init__(self,mongo):
        self.mongo=mongo
    def getSessionId(self,from_dt=None,to_dt=None,refNum=None):
        projection=Constants.USER_DETAILS+"."+Constants.PTSESSIONID #user_details.ptSessionId
        complete_data=self.mongo.query_db(self.get_query(from_dt,to_dt,refNum),projection={projection})
        return [{"id" : data[Constants.USER_DETAILS][Constants.PTSESSIONID]} for data in complete_data  if Constants.USER_DETAILS in data]

    def getConversations(self,session_id=None,from_dt=None,to_dt=None,refNum=None):
        projection=Constants.USER_DETAILS+"."+Constants.BOT_RESPONSE+"."+Constants.MESSAGES
        complete_data=self.mongo.query_db(self.get_query(from_dt,to_dt,refNum,session_id),projection={projection})
        return [data[Constants.USER_DETAILS][Constants.BOT_RESPONSE][Constants.MESSAGES] for data in complete_data]

    def get_query(self,from_dt,to_dt,refNum,session_id=None,):
        query=[]
        if(from_dt!=None):
            query.append({Constants.TIMESTAMP:{"$gt" : datetime.datetime.strptime(from_dt,Constants.DATE_FORMAT)}})
        if(to_dt != None):
            query.append({Constants.TIMESTAMP:{"$lt" : datetime.datetime.strptime(to_dt,Constants.DATE_FORMAT)}})
        if(session_id!=None):
            query.append({Constants.USER_DETAILS+"."+Constants.PTSESSIONID : session_id})
        if(refNum!=None):
            query.append({Constants.USER_DETAILS+"."+Constants+"."+Constants.REFNUM : refNum})


        if(len(query)==0):
            return {}
        return {"$and" : query}

if __name__ == "__main__":
    host =get_db_url()
    db = get_db_name()
    collection = Collections.USER_CONVERSATIONS
    mongo = Mongo(host)
    mongo.get_db(db, collection)
    sessionInfo=sessionInfo(mongo)
    sessionInfo.getSessionId()
    sessionInfo.getConversations("1")

