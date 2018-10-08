import datetime

from mongoQuery import Mongo


class Feedback():
    def __init__(self,mongo):
        self.mongo=mongo
    def get_score(self):
        from_dt=datetime.datetime.strptime('2018-09-06', '%Y-%m-%d')
        times_asked_for_feedback=self.mongo.query_db({ "userConversation.mlModel.modelAction": "ACTION_ASK_FAQ_FEEDBACK" },True)
        times_asked_for_feedback+=self.mongo.query_db({ "userConversation.mlModel.modelAction": "ACTION_ASK_JOBS_FEEDBACK" },True)
        positive_feedback= self.mongo.query_db({ "userConversation.userQuery": "&#x1F44D;" },True)
        negative_feedback= self.mongo.query_db({ "userConversation.userQuery": "&#x1F44E;" },True)
        return(positive_feedback - negative_feedback)/times_asked_for_feedback

if __name__ == "__main__":
    mongo = Mongo(
        "mongodb://esuser:D5l09tt5%24l95n%21@deloitteg-db1.imomentous.co:27017,deloitteg-db2.imomentous.co:27017,deloitteg-db3.imomentous.co:27017/admin?readPreference=primary")
    mongo.get_db("mongo_chatbot", "USER_CONVERSATIONS");
    print("F:",Feedback(mongo).get_score())


