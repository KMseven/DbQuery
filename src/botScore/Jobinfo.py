from constants.Constants import Constants, Collections
from src.botScore.mongoQuery import Mongo
from src.config import get_db_name, get_db_url


class jobinfo():
    def __init__(self,mongo):
        self.mongo=mongo

    def getScore(self,refNum=None):
        document=self.mongo.query_db(self.get_query(refNum),projection={Constants.JOBS_DISPLAYED,Constants.JOB_VIEWS,Constants.APPLY_CLICKS})
        score=[0,0]
        for data in document:
            score[0]+=data[Constants.JOB_VIEWS]/(data[Constants.JOBS_DISPLAYED]+1)
            score[1]+=data[Constants.APPLY_CLICKS]/data[Constants.JOB_VIEWS]
        return score

    def get_query(self,refNum):
        if(refNum!=None):
            return {'_id':refNum}
        return {}



if __name__ == "__main__":
    host =get_db_url()
    db = get_db_name()
    collection = Collections.MISC
    mongo = Mongo(host)
    mongo.get_db(db, collection)
    jobinfo(mongo).getScore("PHENA0059")

