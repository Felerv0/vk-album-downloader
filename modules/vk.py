import configparser
import requests


class VkApi:
    SERVER_ADDRESS = "https://api.vk.com"
    API_VERSION = "5.199"

    def __init__(self, token=None, cfg_file=None):
        self.session = None
        if cfg_file:
            cfg = configparser.ConfigParser()
            cfg.read(cfg_file)
            self.token = str(cfg["VK"]["token"])
        else:
            if token:
                self.token = token
            self.create_session()

    def create_session(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}"
        })

    def request(self, method, params: dict):
        query = "&".join([f"{p}={params[p]}" for p in params])
        return self.session.get(f"{VkApi.SERVER_ADDRESS}/method/{method}?{query}&v={VkApi.API_VERSION}")