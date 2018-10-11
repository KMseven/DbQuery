from botScore.mongoQuery import Mongo

class UnknownIntent():

    def __init__(self,host):
        self.host = host

    def getUidForUnknownIntent(self,db,collection):
        mongo = Mongo(self.host)
        self.collection = mongo.get_db(db,collection)
        docs = self.collection.find({"user_details.botAction":"UTTER_UNINTERPRETABLE"}, {"user_details.ptSessionId":1, "_id":0})
        array = list(docs)
        return array

    def getDocForUid(self,ptSessionQuery):
        ptSessionIdValue = ptSessionQuery['user_details']['ptSessionId']
        docs = self.collection.find({"user_details.ptSessionId":ptSessionIdValue},{"user_details.request":1,"user_details.botResponse.messages":1,"_id":0})
        array = list(docs)
        return array
if __name__==  "__main__":
    obj = UnknownIntent("mongodb://pheglodev:goodDevelopers%401@dev-ng-mongo1.phenompeople.com:27017,dev-ng-mongo2.phenompeople.com:27017,dev-ng-mongo3.phenompeople.com:27017/mongo_ngcc_dev?readPreference=primary");
    array = obj.getUidForUnknownIntent("mongo_chatbot","USER_CONVERSATIONS")
    i = 0;
    while i < len(array) :
        print("id...",array[i])
        arrayObj = obj.getDocForUid(array[i])
        print("result = ",arrayObj)
        i += 1
    print("caller  ends")
