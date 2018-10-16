import logging
import logging.config

import utils.config as config


class Logger(object):
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Logger.__instance == None:
            Logger()
        return Logger.__instance 

    def __init__(self):
        """ Virtually private constructor. """
        if Logger.__instance != None:
            raise Exception("This class is a Logger!")
        else:
            # cherrypy.config.get("log_config_path")
            #/home/vaibhav/repo/user-intent-detection/user-intent-prediction/conf/logging.conf
            logging.config.fileConfig(config.get_log_config_path())
            self.logger = logging.getLogger('fileLogger')
            self.log_err = logging.getLogger('errLogger')
            Logger.__instance = self

