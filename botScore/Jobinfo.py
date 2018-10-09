from botScore.mongoQuery import Mongo


class jobinfo():
    def __init__(self,host,db,collection,refNum="PHENA0059"):
        mongo=Mongo(host)
        mongo.get_db(db, collection)
        self.mongo=mongo
        self.refNum=refNum

    def getScore(self):
        data=self.mongo.query_db(self.get_query(self.refNum))
        return [data[0]["JobViews"]/(data[0]["JobsDisplayed"]+1),data[0]["ApplyClicks"]/data[0]["JobViews"]]


    def get_query(self,client):
        return {'_id':client}



if __name__ == "__main__":
    host="mongodb://esuser:D5l09tt5%24l95n%21@deloitteg-db1.imomentous.co:27017,deloitteg-db2.imomentous.co:27017,deloitteg-db3.imomentous.co:27017/admin?readPreference=primary"
    db="mongo_chatbot"
    collection="MISC"
    jobinfo(host,db,collection).getScore("PHENA0059")

