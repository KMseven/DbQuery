import json
import threading

from kafka import KafkaConsumer
from botScore.mongoQuery import Mongo


class Consumer(threading.Thread):
    daemon = True
    def __init__(self,host,db,collection):
        threading.Thread.__init__(self)
        mongo=Mongo(host)
        mongo.get_db(db, collection)
        self.mongo=mongo
        self.count=0
        self.count1=0
        self.count2=0
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers="dev-kafka01:9092",
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=True,
                                 group_id='my-group',
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')))

        consumer.subscribe(["Phenom_Track_PHENA0059_TOPIC", "Phenom_Track_ESMEUS_TOPIC", "Phenom_Track_EVCOUS_TOPIC",
                            "Phenom_Track_HEFIUS_TOPIC"])

        for message in consumer:
            self.count+=1
            client=message.value["clientToken"]
            if (message.value["event"] == "job_click"):
                mongo.update_db(self.create_query(client,"JobViews"))
            elif(message.value["event"] == "apply_click"):
                mongo.update_db(self.create_query(client,"ApplyClicks"))



    def create_query(self,id,value):
        return {"_id" : id},{"$inc" : {value : 1}}


""



if __name__ == "__main__":
    host="mongodb://esuser:D5l09tt5%24l95n%21@deloitteg-db1.imomentous.co:27017,deloitteg-db2.imomentous.co:27017,deloitteg-db3.imomentous.co:27017/admin?readPreference=primary"
    db="mongo_chatbot"
    collection="MISC"
    threads = Consumer(host,db,collection)
    threads.start()
    while threads.is_alive():
        threads.join()




