import json
import threading

from kafka import KafkaConsumer

from constants.Constants import Collections
from src.botScore.mongoQuery import Mongo
from src.config import get_db_name, get_db_url


class Consumer(threading.Thread):
    daemon = True
    def __init__(self,mongo):
        threading.Thread.__init__(self)
        self.mongo=mongo

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
                self.mongo.update_db(self.create_query(client,"JobViews"))
            elif(message.value["event"] == "apply_click"):
                self.mongo.update_db(self.create_query(client,"ApplyClicks"))



    def create_query(self,id,value):
        return {"_id" : id},{"$inc" : {value : 1}}



if __name__ == "__main__":
    host =get_db_url()
    db = get_db_name()
    collection = Collections.USER_CONVERSATIONS
    mongo = Mongo(host)
    mongo.get_db(db, collection)
    threads = Consumer(mongo)
    threads.start()
    while threads.is_alive():
        threads.join()




