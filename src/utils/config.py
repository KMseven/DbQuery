import json
import os
from constants.constants import Constants
config = None
s3_config = None
override_nlu_config = dict()

def check_string_null(string):
    if string.strip() == "":
        return None
    if string is None:
        return None
    return string


def read_config_file():
    global config
    if config:
        return config
    else:
        with open(os.path.join(os.curdir, 'conf/configFile.json'),
                  mode='r') as json_data_file:
            config = json.load(json_data_file)
            return config

def update_config_file():
    global config
    with open(os.path.join(os.curdir, 'conf/configFile.json'),
              mode='r') as json_data_file:
        config = json.load(json_data_file)
    return True



def read_s3_config_file():
    global s3_config
    if s3_config:
        return s3_config
    else:
        with open('/home/gaurav/bots/user-intent-prediction/conf/s3_bucket.json',
                  mode='r') as json_data_file:
            s3_config = json.load(json_data_file)
            return s3_config


def get_log_config_path():
    data = read_config_file()
    return data['log_config_path']


def get_path_to_model():
    data = read_config_file()
    return data['path_to_model']


def get_model_config_url():
    data = read_config_file()
    return data['model_config_url']


def get_sentence_vector_url():
    data = read_config_file()
    return data['sentence_vector_url']


def get_slideRadius():
    data = read_config_file()
    return data['slideRadius']

def get_db_uri():
    data = read_config_file()
    return data['db_uri']

def get_job_update_log_collection():
    data = read_config_file()
    return data['db_collection_jobs_update_log']



def get_phenom_track_api():
    data = read_config_file()
    return data['phenom_track_api']


def get_socket_port():
    data = read_config_file()
    return data['socket_port']


def get_socket_host():
    data = read_config_file()
    return data['socket_host']


def get_use_redis_for_tracker_store():
    data = read_config_file()
    return data['use_redis_for_tracker_store']


def get_redis_host():
    data = read_config_file()
    return data['redis_host']


def get_redis_port():
    data = read_config_file()
    return data['redis_port']


def get_redis_password():
    data = read_config_file()
    return data['redis_password']

def get_redis_db():
    data = read_config_file()
    return data['redis_db']

def get_sentence_vector_entity_url():
    data = read_config_file()
    return data['sentence_vector_entity_url']


def get_country_mapping_file_path():
    data = read_config_file()
    return data["country_mapping_file_path"]


def get_conditions_file_path():
    data = read_config_file()
    return data["conditions_file_path"]


def get_nlu_model_path():
    data = read_config_file()
    return data["nlu_model_path"]


def get_dm_model_path():
    data = read_config_file()
    return data["dm_model_path"]


def get_s3_config_path():
    data = read_config_file()
    return data['s3_config_path']


def get_storage():
    data = read_config_file()
    return data['storage']


def get_project_name():
    data = read_config_file()
    return data['project_name']


def get_dm_model_prefix():
    data = read_config_file()
    return data['dm_model_prefix']


def get_nlu_model_prefix():
    data = read_config_file()
    return data['nlu_model_prefix']


def get_s3_bucket_name():
    data = read_s3_config_file()
    return data['BUCKET_NAME']


def get_s3_aws_region():
    data = read_s3_config_file()
    return data['AWS_REGION']


def get_s3_aws_access_key_id():
    data = read_s3_config_file()
    return data['AWS_ACCESS_KEY_ID']

def get_redis_pubsub_channel_name():
    data = read_config_file()
    return data['redis_pubsub_channel_name']

def get_redis_job_pull_host():
    data = read_config_file()
    return data['redis_job_pull_host']

def get_db_database_job_pull():
    data = read_config_file()
    return data['db_database_job_pull']

def get_db_database_chatbot():
    data = read_config_file()
    return data['db_database_chatbot']

def get_db_collection_jobs_update_log():
    data = read_config_file()
    return data['db_collection_jobs_update_log']

def get_db_collection_jobs_information():
    data = read_config_file()
    return data['db_collection_jobs_information']

def get_db_collection_bot_config():
    data = read_config_file()
    return data['db_collection_bot_config']

def get_redis_job_pull_port():
    data = read_config_file()
    return data['redis_job_pull_port']





def get_s3_aws_secret_access_key():
    data = read_s3_config_file()
    return data['AWS_SECRET_ACCESS_KEY']

def get_override_nlu_path():
    data = read_config_file()
    return data['override_nlu_path']

def get_fasttext_model_path():
    data = read_config_file()
    return data['fastext_model_path']



def update_nlu_override_config(refNum,newCategories):
    global override_nlu_config
    for dic in override_nlu_config['data']:
        if Constants.ref_num in dic and Constants.values in dic:
            if dic[Constants.ref_num]==refNum:
                newCategories = newCategories + Constants.All_Categories
                dic[Constants.values]=newCategories
                dic['type']='quickreply'