import json

config=None
def read_config_file():
    global config
    if config:
        return config
    else:
        with open("/home/krishna_mohan/PycharmProjects/botScore/config/configFile.json",mode='r') as json_data_file:
            config = json.load(json_data_file)
            return config

def get_db_url():
    data=read_config_file()
    data["mongo_url"]

def get_db_name():
    data=read_config_file()
    data["mongo_db_name"]





if __name__ == "__main__":
    get_db_url()
