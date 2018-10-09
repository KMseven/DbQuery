import json
import threading

from kafka import KafkaConsumer
import time
from mongoQuery import Mongo


class Consumer(threading.Thread):
    daemon = True
    def __init__(self,mongo):
        threading.Thread.__init__(self)
        self.mongo=mongo
        self.count=0
        self.count1=0
        self.count2=0
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers="dev-kafka01:9092",
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=True,
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')))

        consumer.subscribe(["Phenom_Track_PHENA0059_TOPIC", "Phenom_Track_ESMEUS_TOPIC", "Phenom_Track_EVCOUS_TOPIC",
                            "Phenom_Track_HEFIUS_TOPIC"])

        for message in consumer:
            self.count+=1
            client=message.value["clientToken"]
            if (message.value["event"] == "job_click"):
                self.count1+=1
                mongo.update_db(self.create_query(client,"JobViews"))
            elif(message.value["event"] == "apply_click"):
                self.count2+=1
                mongo.update_db(self.create_query(client,"ApplyClicks"))
            print(self.count,self.count1,self.count2)

    def create_query(self,id,value):
        return {"_id" : id},{"$inc" : {value : 1}}


""



if __name__ == "__main__":
    mongo = Mongo(
        "mongodb://pheglodev:goodDevelopers%401@dev-ng-mongo1.phenompeople.com:27017,dev-ng-mongo2.phenompeople.com:27017,dev-ng-mongo3.phenompeople.com:27017/mongo_ngcc_dev?readPreference=primary")
    mongo.get_db("mongo_chatbot", "MISC")
    threads = Consumer(mongo)
    threads.start()
    while threads.is_alive():
        threads.join()




