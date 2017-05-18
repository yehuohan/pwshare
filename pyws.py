
#===============================================================================
# file   : WifiShare.py
# brief  : WifiShare module used in windows
# e-mail : 550034086@qq.com, yehuohan@gmail.com
# author : yehuohan
#===============================================================================


#===============================================================================
# import
#===============================================================================
import os
import subprocess
import json

#===============================================================================
# WsJson class
#===============================================================================
class WsJson:
    __filename = "pws.json"
    __main_key = None
    cf = None
    cf_defalut = {
        "pws.json": [
            "WifiShare",
            "Gui-qt",
            "Gui-tk"
        ],
        "WifiShare": {
            "ssid": "ubuntu",
            "key": "uuuuuuuu"
        },
        "Gui-qt": {
            "showpw": "True"
        },
        "Gui-tk": {}
    }

    def __init__(self, index_key):
        if False == os.path.exists(self.__filename):
            self.make_default()
        self.__main_key = index_key
        with open(self.__filename, "r", encoding="utf-8") as load_f:
            self.cf = json.load(load_f)

    def make_default(self):
        with open(self.__filename, "w", encoding="utf-8") as dump_f:
            json.dump(self.cf_defalut, dump_f)

    def get_value(self, key):
        return self.cf[self.__main_key][key]

    def put_value(self, key, value):
        with open(self.__filename, "w", encoding="utf-8") as dump_f:
            self.cf[self.__main_key][key] = value
            json.dump(self.cf, dump_f)


#===============================================================================
# WifiShare class
#===============================================================================
class WifiShare:
    __wj = WsJson("WifiShare")
    ssid = None
    key = None

    def __init__(self):
        self.set_ssid(self.__wj.get_value("ssid"))
        self.set_key(self.__wj.get_value("key"))

    def set_ssid(self, s):
        if s!= "":
            self.ssid = s

    def set_key(self, k):
        if k != "":
            self.key = k

    def create_wifi(self, s = "", k = ""):
        self.set_ssid(s)
        self.set_key(k)
        self.save_set()
        return subprocess.getstatusoutput("netsh wlan set hostednetwork mode=allow ssid={s} key={k}".format(s = self.ssid, k = self.key))

    def start_wifi(self):
        return subprocess.getstatusoutput("netsh wlan start hostednetwork")

    def stop_wifi(self):
        return subprocess.getstatusoutput("netsh wlan stop hostednetwork")

    def close_wifi(self):
        return subprocess.getstatusoutput("netsh wlan set hostednetwork mode=disallow")

    # save the ssid and key to the json configuration
    def save_set(self):
        self.__wj.put_value("ssid", self.ssid)
        self.__wj.put_value("key", self.key)

