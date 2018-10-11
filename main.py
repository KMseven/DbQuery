import json

from flask import request
from flask import Flask

from botScore.mongoQuery import Mongo
from sessioninfo.sessionInfo import sessionInfo

app = Flask(__name__)
host = "mongodb://pheglodev:goodDevelopers%401@dev-ng-mongo1.phenompeople.com:27017,dev-ng-mongo2.phenompeople.com:27017,dev-ng-mongo3.phenompeople.com:27017/mongo_ngcc_dev?readPreference=primary"
db="mongo_chatbot"

@app.route("/")
def test():
    return "Running"

@app.route("/session_id",methods=['POST'])
def getSessionInfo():
    content=request.get_json()
    collection="USER_CONVERSATIONS"
    mongo = Mongo(host)
    mongo.get_db(db, collection)
    data = sessionInfo(host, db, collection,content["refNum"]).getSessionId(content["from"],content["to"])
    return json.dumps(data)

@app.route("/conversations",methods=["POST"])
def getCoversations():
    content=request.get_json()

if __name__== "__main__":
    mongo = Mongo(host)
    app.run(host='localhost', port=5000, debug=True)