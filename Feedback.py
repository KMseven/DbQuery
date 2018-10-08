import datetime

from mongoQuery import Mongo


class Feedback():
    def __init__(self,mongo):
        self.mongo=mongo
    def get_score(self):
        from_dt=datetime.datetime.strptime('2018-09-06', '%Y-%m-%d')


if __name__ == "__main__":
    mongo = Mongo(
        "mongodb://pheglodev:goodDevelopers%401@dev-ng-mongo1.phenompeople.com:27017,dev-ng-mongo2.phenompeople.com:27017,dev-ng-mongo3.phenompeople.com:27017/mongo_ngcc_dev?readPreference=primary")
    mongo.get_db("mongo_chatbot", "users");
    print("F:",Feedback(mongo).get_score())
