from botScore.Feedback import Feedback
from botScore.Jobinfo import jobinfo
from botScore.leadgen import leadgen


class botscore():
    def __init__(self):
        self.host="mongodb://pheglodev:goodDevelopers%401@dev-ng-mongo1.phenompeople.com:27017,dev-ng-mongo2.phenompeople.com:27017,dev-ng-mongo3.phenompeople.com:27017/mongo_ngcc_dev?readPreference=primary"
        self.db="mongo_chatbot"
    def getScore(self):
        A=0
        B=0
        C=0
        [D,E]=jobinfo(self.host, self.db, "MISC").getScore("PHENA0059")
        F=leadgen(self.host, self.db, "users").get_score()
        G=Feedback(self.host, self.db, "USER_CONVERSATIONS").get_score()
        return 0.02 * A + 0.04 * B + 0.06 * C + 0.08 * D + 0.2 * E + 0.3 * F + 0.3 * G


if __name__ == "__main__":
    print(botscore().getScore())