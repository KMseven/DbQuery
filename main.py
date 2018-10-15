import json

from flask import request
from flask import Flask

from botScore.mongoQuery import Mongo
from sessioninfo.sessionInfo import sessionInfo
from unknownIntents.UnknownIntent import UnknownIntent
from botScore.botscore import  botscore

app = Flask(__name__)
host = "mongodb://pheglodev:goodDevelopers%401@dev-ng-mongo1.phenompeople.com:27017,dev-ng-mongo2.phenompeople.com:27017,dev-ng-mongo3.phenompeople.com:27017/mongo_ngcc_dev?readPreference=primary"
db="mongo_chatbot"
collection = "USER_CONVERSATIONS"

@app.route("/")
def test():
    return "Running"

@app.route("/users",methods=['POST'])
def getSessionInfo():
    content=request.get_json()
    mongo = Mongo(host)
    mongo.get_db(db, collection)
    data = sessionInfo(host, db, collection,content["refNum"]).getSessionId(content["from"],content["to"])
    return json.dumps(data)


@app.route("/<session>/conversations",methods=["POST"])
def getCoversations(session):
    content=request.get_json()
    #collection="USER_CONVERSATIONS"
    data = UnknownIntent(host,db,collection).getDocForUid(session,content["from"],content["to"],content["refNum"])
    return json.dumps(data)

@app.route("/unknown_response",methods=["POST"])
def getUnknownIntent():
    content=request.get_json()
    #collection="USER_CONVERSATIONS"
    data = UnknownIntent(host,db,collection).getUidForUnknownIntent(content["from"],content["to"],content["refNum"])
    return json.dumps(data)

@app.route("/bot_score", methods=["POST"])
def getBotScore():
    data = botscore(host,db)
    return json.dumps(data)

if __name__== "__main__":
    mongo = Mongo(host)
    app.run(host='localhost', port=5000, debug=True)