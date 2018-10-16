import json

from flask import request
from flask import Flask

from constants.Constants import Collections
from src.botScore.mongoQuery import Mongo
from src.config import get_db_url, get_db_name
from src.sessioninfo.sessionInfo import sessionInfo
from src.unknownIntents.UnknownIntent import UnknownIntent
from src.botScore.botscore import  botscore

app = Flask(__name__)
host = None
db=None
collection = None
mongo = None

@app.route("/")
def test():
    return "Running"

@app.route("/users",methods=['POST'])
def getSessionInfo():
    content=request.get_json()
    data = sessionInfo(mongo).getSessionId(content["from"],content["to"],content["refNum"])
    return json.dumps(data)


@app.route("/<session>/conversations",methods=["POST"])
def getCoversations(session):
    content=request.get_json()
    data = UnknownIntent(mongo).getDocForUid(session,content["from"],content["to"],content["refNum"])
    return json.dumps(data)

@app.route("/unknown_response",methods=["POST"])
def getUnknownIntent():
    content=request.get_json()
    data = UnknownIntent(host,db,collection).getUidForUnknownIntent(content["from"],content["to"],content["refNum"])
    return json.dumps(data)

@app.route("/bot_score", methods=["POST"])
def getBotScore():
    data = botscore(mongo,db)
    return json.dumps(data)

if __name__== "__main__":
    host =get_db_url()
    db = get_db_name()
    collection = Collections.USER_CONVERSATIONS
    mongo = Mongo(host)
    mongo.get_db(db, collection)
    app.run(host='localhost', port=5000, debug=True)