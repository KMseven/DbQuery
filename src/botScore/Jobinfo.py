from constants.Constants import Constants, Collections
from src.botScore.mongoQuery import Mongo
from src.config import get_db_name, get_db_url
from utils import MongoUtils


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

    @staticmethod
    def get_refNum_query(refNum=None):
        query = {}
        if refNum is not None:
            query['_id'] = refNum
            return query
        return query

    @staticmethod
    def get_jobsinfo_score(refNum=None):
        client_stats = {}
        documents = None
        if refNum is not None:
            documents = MongoUtils.query_db(jobinfo.get_refNum_query(refNum=refNum),
                                            projection={Constants.JOBS_DISPLAYED, Constants.JOB_VIEWS,
                                                        Constants.APPLY_CLICKS,'refNum'})
        for doc in documents:
            ref = doc['refNum']
            no_of_jobs_viewed = doc[Constants.JOB_VIEWS]/(doc[Constants.JOBS_DISPLAYED]+1)
            no_of_applies = doc[Constants.APPLY_CLICKS]/doc[Constants.JOB_VIEWS]
            client_stats[ref] = (no_of_jobs_viewed,no_of_applies)
        return client_stats[refNum]


if __name__ == "__main__":
    host =get_db_url()
    db = get_db_name()
    collection = Collections.MISC
    mongo = Mongo(host)
    mongo.get_db(db, collection)
    jobinfo(mongo).getScore("PHENA0059")

