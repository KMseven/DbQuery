import datetime

from constants.Constants import Constants, Collections
from src.botScore.mongoQuery import Mongo
from src.config import get_db_name, get_db_url


class Feedback():
    def __init__(self,mongo):
        self.mongo=mongo

    def get_score(self,from_dt=None,to_dt=None,refNum=None):
        times_asked_for_feedback=self.mongo.query_db(self.generate_query(from_dt,to_dt,Constants.ACTION_ASK_FAQ_FEEDBACK,refNum),True)
        times_asked_for_feedback+=self.mongo.query_db(self.generate_query(from_dt,to_dt,Constants.ACTION_ASK_JOBS_FEEDBACK,refNum),True)
        positive_feedback= self.mongo.query_db(self.generate_query(from_dt,to_dt,refNum=refNum,user_query=Constants.LIKE),True)
        negative_feedback= self.mongo.query_db(self.generate_query(from_dt,to_dt,refNum=refNum,user_query=Constants.DISLIKE),True)
        return(positive_feedback - negative_feedback)/times_asked_for_feedback


    def generate_query(self,from_dt,to_dt,action=None,refNum="PHENA0059",user_query=None):
        query=[]
        if(from_dt!=None):
            query.append({Constants.TIMESTAMP:{"$gt" : datetime.datetime.strptime(from_dt,Constants.DATE_FORMAT)}})
        if(to_dt != None):
            query.append({Constants.TIMESTAMP:{"$lt" : datetime.datetime.strptime(to_dt,Constants.DATE_FORMAT)}})
        if(refNum!=None):
            query.append({"user_details.refNum": refNum})
        if(action!=None):
            query.append({"userConversation.mlModel.modelNextAction": action})
        else:
            if (user_query != None):
                query.append({"userConversation.userQuery": user_query})

        if(len(query)==0):
            return {}
        return {"$and" : query}


if __name__ == "__main__":
    host =get_db_url()
    db = get_db_name()
    collection = Collections.USER_CONVERSATIONS
    mongo = Mongo(host)
    mongo.get_db(db, collection)
    print("G:",Feedback(mongo).get_score("PHENA0059"))


