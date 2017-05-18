
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
    # hostednetwork status information
    hn_status = {}
    ssid = None
    key = None

    def __init__(self):
        self.set_ssid(self.__wj.get_value("ssid"))
        self.set_key(self.__wj.get_value("key"))
        self.get_hn_status()
        if self.is_started():
            self.set_ssid(self.get_ssidname())

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
        ret = subprocess.getstatusoutput("netsh wlan set hostednetwork mode=allow ssid={s} key={k}".format(s = self.ssid, k = self.key))
        self.get_hn_status()
        return ret

    def start_wifi(self):
        ret = subprocess.getstatusoutput("netsh wlan start hostednetwork")
        self.get_hn_status()
        return ret

    def stop_wifi(self):
        ret = subprocess.getstatusoutput("netsh wlan stop hostednetwork")
        self.get_hn_status()
        return ret

    def close_wifi(self):
        ret = subprocess.getstatusoutput("netsh wlan set hostednetwork mode=disallow")
        self.get_hn_status()
        return ret

    def show_wifi(self):
        return subprocess.getstatusoutput("netsh wlan show hostednetwork")

    # get hostednetwork show information
    def get_hn_status(self):
        ret = self.show_wifi()
        ret_lst = [] 
        if ret[0] == 0:
            for ele in ret[1].replace(" ", "").split("\n"):
                if 1 == ele.count(":"):
                    ret_lst += [ele.split(":"),]
            self.hn_status = dict(ret_lst)
            return True
        else:
            return False

    # save the ssid and key to the json configuration
    def save_set(self):
        self.__wj.put_value("ssid", self.ssid)
        self.__wj.put_value("key", self.key)

    #===========================================================================
    # functions below only ofr windows in Chinese Lauguage
    #===========================================================================

    # check if wifi is started
    def is_started(self):
        if self.hn_status["状态"] == "已启动":
            return True
        else:
            return False

    # get ssid name if wifi is already started
    def get_ssidname(self):
        if self.is_started():
            return self.hn_status["SSID名称"].replace('“', "").replace('”', "")

    # get user(client) number
    def get_user_num(self):
        if self.is_started():
            return self.hn_status["客户端数"]


#===============================================================================
# main-loop for test
#===============================================================================
if __name__ == "__main__":
    ws = WifiShare()
    print(ws.is_started())
    print(ws.get_user_num())
    print(ws.get_ssidname())
    print(ws.hn_status)
