import json


class DefaultConfig():
    def __init__(self):
        with open("./config/default_config.json", "r", encoding="utf-8") as file:
            config = json.load(file)
        if not config:
            raise Exception("Config is empty, you maggot")
        self.__default_json = config

    def get_default(self):
        return self.__default_json