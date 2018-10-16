import json
import re

from pymongo import MongoClient

import utils.config as config

# import utils.httphelper as httphelper
client = MongoClient(
        host=config.get_db_uri())


def get_jobs_update_log_document(refNum,time_stamp):
    db = client.get_database(config.get_db_database_job_pull())
    collection = db.get_collection(config.get_job_update_log_collection())
    doc = collection.find_one({"refNum": refNum,"timestamp":time_stamp})
    return doc

def get_jobs_category(refNum):
    db = client.get_database(config.get_db_database_job_pull())
    collection = db.get_collection(config.get_db_collection_jobs_information())
    doc = collection.distinct("category",{"refNum": refNum})
    return doc


def get_jobs_countries(refNum):
    db = client.get_database(config.get_db_database_job_pull())
    collection = db.get_collection(config.get_db_collection_jobs_information())
    doc = collection.distinct("country",{"refNum": refNum})
    return doc

def get_bot_clients_list(refNum=None):
    db = client.get_database(config.get_db_database_chatbot())
    collection = db.get_collection(config.get_db_collection_bot_config())
    if refNum is not None:
        doc = collection.find({"_id": refNum})
    else:
        doc = collection.distinct("_id")
    return doc

def get_all_configs_collection():
    db = client.get_database(config.get_db_database_chatbot())
    collection = db.get_collection(config.get_db_collection_bot_config())
    return collection

def all_clients(configurations):
        clients = configurations.distinct("_id")
        return clients


def client_config_countryMapping(collection,refNum):
        print (refNum)
        countryMapping = [val for val in collection.find({"_id": refNum}, {"serverConfigurations.countryMapping": 1})][0]["serverConfigurations"]["countryMapping"]
        return countryMapping

def getLocationsFromMongo(placeId):
    response={}
    locations= []
    db = client.get_database("mongo_ngcc_dev")
    collection = db.get_collection("jobs_locations")
    doc = collection.find_one({"placeId": placeId})
    if doc["type"]=="country" or doc[type]=="state":
        for i in doc["all_names"]:
             locations.append(i)
    else:
        locations.append(doc["key"])
    response["locations"]=locations
    response["type"]=doc["type"]
    response["placeId"]=placeId
    return response

def getEntitiesFromMongo():
    db = client.get_database("mongo_px_team")
    collection = db.get_collection("nlu_training_data")
    p = re.compile("entity")
    # docs =
    data={}
    data["rasa_nlu_data"]={}
    data["rasa_nlu_data"]["common_examples"]=[]
    for doc in collection.find({"version" : "version2"}):
        new_data={}
        new_data["text"]=doc["query"]
        new_data["entities"]=[]
        new_data["intent"]=doc["intent"]
        if doc["intent"]=="entity_search" or doc["intent"]=="negation_search":
            for m in p.finditer(doc["query"]):
                print(m.start(), m.group())
                entities={}
                entities["start"] =m.start()
                entities["end"] =m.start()+6
                entities["value"] ="entity"
                entities["entity"] = "entity"
                new_data["entities"].append(entities)
        data["rasa_nlu_data"]["common_examples"].append(new_data)

    with open('result.json', 'w') as fp:
        json.dump(data, fp)

def getEntities():
    db = client.get_database("mongo_px_team")
    collection = db.get_collection("nlu_training_data")
    p = re.compile("entity")
    # docs =
    data={}
    data["keywords_array"]=[]
    for doc in collection.find({"version" : "version2"}):
        new_data={}
        new_data["query"]=doc["query"]
        new_data["intent"]=doc["intent"]
        data["keywords_array"].append(new_data)

    # data=httphelper.postlocal("http://192.168.255.97:8080/rasa_entities",data)
    with open('result.json', 'w') as fp:
        json.dump(data, fp)

def get_faqs(refNum=None):
    db = client.get_database('mongo_chatbot')
    collection = db.get_collection('faqs')
    if refNum is not None:
        data = collection.find({"refNum" : refNum})
    else:
        data = collection.find({"refNum" : "default"},{"faqType":1,"botFaqVariations":1,"refNum":1})
    # else:
    #     data = collection.find({})
    return data

def query_db(query,get_length=False,projection={},collection_name=None):
    collection = None
    db = client.get_database('mongo_chatbot')
    if collection_name is not None:
        collection = db.get_collection(collection_name)
    if(get_length):
        return collection.find(query).count()
    complete_data=[]
    for data in collection.find(query,projection):
        complete_data.append(data)
    return complete_data

def write_db(query,collection_name=None):
    db = client.get_database('mongo_chatbot')
    if collection_name is not None:
        collection = db.get_collection(collection_name)
        collection.insert(query)

def update_db(query,collection_name=None):
    db = client.get_database('mongo_chatbot')
    if collection_name is not None:
        collection = db.get_collection(collection_name)
        collection.insert(query)
        collection.update_one(query[0],query[1], upsert=True)

def insert_db(document,collection_name=None):
    db = client.get_database('mongo_chatbot')
    if collection_name is not None:
        collection = db.get_collection(collection_name)
        collection.insert(document)




if __name__ == '__main__':
    # getLocationsFromMongo("ChIJQ4Ld14-UC0cRb1jb03UcZvg")
    # getEntitiesFromMongo()
   response= get_bot_clients_list()
   print(response)
    # matches = re.findall("entity", "I want entity jobs")
    # print(matches.__getitem__(0).)