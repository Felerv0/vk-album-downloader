from configparser import ConfigParser

CONFIG = ConfigParser()
CONFIG.read("config.ini")

TOKEN = open("token.txt").readline().strip()

MAX_PHOTO_COUNT_PER_REQUEST = int(CONFIG["CONSTS"]["MAX_PHOTO_PER_REQUEST"])
DOWNLOAD_DELAY_API = float(CONFIG["CONSTS"]["DOWNLOAD_DELAY_API"])
DOWNLOAD_GROUP_DELAY = float(CONFIG["CONSTS"]["DOWNLOAD_GROUP_DELAY"])
WRITE_DESCRIPTION = bool(CONFIG["CONSTS"]["WRITE_DESCRIPTION"])