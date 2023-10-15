
import json

class Configuration():
  configFilePath = "./config/config.json"

  @staticmethod
  def getValue(key:str):
    """This method is getting value by key from config file on demand. 
    Config is not fixed on start and can be hot edited
    """
    with open(Configuration.configFilePath) as configFile:
      config = json.loads(configFile.read())
    return config[key]
