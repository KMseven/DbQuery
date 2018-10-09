import datetime

from botScore.mongoQuery import Mongo
class Feedback():
    def __init__(self,host,db,collection):
        mongo=Mongo(host)
        mongo.get_db(db, collection)
        self.mongo=mongo
    def get_score(self,from_dt='2018-09-06',to_dt='2018-09-06'):
        from_dt=datetime.datetime.strptime(from_dt, '%Y-%m-%d')
        to_dt=datetime.datetime.strptime(to_dt, '%Y-%m-%d')
        times_asked_for_feedback=self.mongo.query_db({ "userConversation.mlModel.modelNextAction": "ACTION_ASK_FAQ_FEEDBACK" },True)
        times_asked_for_feedback+=self.mongo.query_db({ "userConversation.mlModel.modelNextAction": "ACTION_ASK_JOBS_FEEDBACK" },True)
        positive_feedback= self.mongo.query_db({ "userConversation.userQuery": "&#x1F44D;" },True)
        negative_feedback= self.mongo.query_db({ "userConversation.userQuery": "&#x1F44E;" },True)
        return(positive_feedback - negative_feedback)/times_asked_for_feedback
if __name__ == "__main__":
    host="mongodb://esuser:D5l09tt5%24l95n%21@deloitteg-db1.imomentous.co:27017,deloitteg-db2.imomentous.co:27017,deloitteg-db3.imomentous.co:27017/admin?readPreference=primary"
    db="mongo_chatbot"
    collection="USER_CONVERSATIONS"
    print("G:",Feedback(host,db,collection).get_score())


