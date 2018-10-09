import datetime

from botScore.mongoQuery import Mongo
class Feedback():
    def __init__(self,host,db,collection,refNum="PHENA0059"):
        mongo=Mongo(host)
        mongo.get_db(db, collection)
        self.mongo=mongo
        self.refNum=refNum
    def get_score(self,from_dt='2018-09-06',to_dt='2018-09-06'):
        from_dt=datetime.datetime.strptime(from_dt, '%Y-%m-%d')
        to_dt=datetime.datetime.strptime(to_dt, '%Y-%m-%d')
        times_asked_for_feedback=self.mongo.query_db(self.get_query({ "userConversation.mlModel.modelNextAction": "ACTION_ASK_FAQ_FEEDBACK" },from_dt,to_dt),True)
        times_asked_for_feedback+=self.mongo.query_db(self.get_query({ "userConversation.mlModel.modelNextAction": "ACTION_ASK_JOBS_FEEDBACK" },from_dt,to_dt),True)
        positive_feedback= self.mongo.query_db(self.get_query({ "userConversation.userQuery": "&#x1F44D;" },from_dt,to_dt),True)
        negative_feedback= self.mongo.query_db(self.get_query({ "userConversation.userQuery": "&#x1F44E;" },from_dt,to_dt),True)
        return(positive_feedback - negative_feedback)/times_asked_for_feedback

    def get_query(self,data,from_dt,to_dt):
        query={ "$and": [{"timeStamp": { "$gt": from_dt}}, {"timeStamp": { "$lt": to_dt}, "refNum": self.refNum}]}
        for key in data.keys():
            query[key]=data[key]
if __name__ == "__main__":
    host="mongodb://esuser:D5l09tt5%24l95n%21@deloitteg-db1.imomentous.co:27017,deloitteg-db2.imomentous.co:27017,deloitteg-db3.imomentous.co:27017/admin?readPreference=primary"
    db="mongo_chatbot"
    collection="USER_CONVERSATIONS"
    print("G:",Feedback(host,db,collection).get_score())


