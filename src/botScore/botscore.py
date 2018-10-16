from constants.Constants import Collections
from src.botScore.Feedback import Feedback
from src.botScore.Jobinfo import jobinfo
from src.botScore.leadgen import leadgen
from src.botScore.mongoQuery import Mongo
from src.config import get_db_name, get_db_url


class botscore():
    def __init__(self,mongo,db):
        self.mongo=mongo
        self.db=db
    def getScore(self,refNum=None,from_dt=None,to_dt=None):
        A=0
        B=0
        C=0
        [D,E]=jobinfo(self.setDatabase(Collections.MISC)).getScore(refNum)
        F=leadgen(self.setDatabase(Collections.users)).get_score(from_dt,to_dt,refNum=refNum)
        G=Feedback(self.setDatabase(Collections.USER_CONVERSATIONS)).get_score(from_dt,to_dt,refNum=refNum)
        return 0.02 * A + 0.04 * B + 0.06 * C + 0.08 * D + 0.2 * E + 0.3 * F + 0.3 * G

    def setDatabase(self,collection):
        self.mongo.get_db(self.db,collection)
        return self.mongo


if __name__ == "__main__":
    host =get_db_url()
    db =get_db_name()
    collection = Collections.USER_CONVERSATIONS
    mongo = Mongo(host)
    mongo.get_db(db, collection)
    print(botscore(mongo).getScore("PHENA0059"))