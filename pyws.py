
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
import ctypes


#===============================================================================
# WsJson class
#===============================================================================
class WsJson:
    __filename = "pws.json"
    __main_key = None

    # all settings in .json will set to cf
    cf = None
    cf_defalut = {
        "pws.json": [
            "WifiShare",
            "Gui-qt",
            "Gui-tk"
        ],
        "WifiShare": {
            "ssid": "ubuntu",
            "key": "uuuuuuuu",
            "eth_name":"以太网"
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

    # create .json with cf_default if there is no .json file
    def make_default(self):
        with open(self.__filename, "w", encoding="utf-8") as dump_f:
            json.dump(self.cf_defalut, dump_f)

    # get key-value in main_key
    def get_value(self, key):
        return self.cf[self.__main_key][key]

    # put key-value in main_key
    def put_value(self, key, value):
        with open(self.__filename, "w", encoding="utf-8") as dump_f:
            self.cf[self.__main_key][key] = value
            json.dump(self.cf, dump_f)


#===============================================================================
# WsDll class 
#===============================================================================
class WsDll:
    __wsdll = None

    def __init__(self, path = "ws.dll"):
        self.__wsdll = ctypes.windll.LoadLibrary(path)

    #===========================================================================
    # the return value of functions below in this format
    # format       : return (bool, function-ret, user-args)
    # bool         : Report function is execute successful or not
    # function-ret : Value function return, who's meanings can be found in dll's header-file
    # user-args    : What user expect function return. May more than one
    #===========================================================================

    # start connection sharing of ethernet and hostednetwork
    def start_connection_sharing(self, eth_name):
        name_p = ctypes.c_wchar_p()
        name_p.value = eth_name;
        ret = self.__wsdll.ws_enable_sharing(name_p)
        if(0 == ret):
            return (True, ret)
        else:
            return (False, ret)

    # close connection sharing of ethernet and hostednetwork
    def close_connection_sharing(self, eth_name):
        name_p = ctypes.c_wchar_p()
        name_p.value = eth_name;
        ret = self.__wsdll.ws_disable_sharing(name_p)
        if(0 == ret):
            return (True, ret)
        else:
            return (False, ret)

    # get all connections's name to choose eth_name
    def get_connections(self):
        ret = ctypes.c_int()
        self.__wsdll.ws_py_get_connections.restype = ctypes.py_object
        cons = self.__wsdll.ws_py_get_connections(ctypes.byref(ret))
        if(0 == ret.value):
            # return result if get connections successful
            return (True, ret.value, cons)
        else:
            return (False, ret.value)

    # report whether the operating-system supporting connection sharing
    def is_support_connection_sharing(self):
        flg = ctypes.c_bool()
        ret = self.__wsdll.ws_support_connection_sharing(ctypes.byref(flg))
        if(0 == ret):
            # flg is meaningful when function is executed successful
            return (True, ret, bool(flg.value))
        else:
            return (False, ret)


#===============================================================================
# WifiShare class
#===============================================================================
class WifiShare:
    __wj = WsJson("WifiShare")
    __wd = WsDll("ws.dll")
    # hostednetwork status information
    hn_status = {}
    ssid = None
    key = None
    # the name of the connection to be shared
    eth_name = None

    def __init__(self):
        self.set_ssid(self.__wj.get_value("ssid"))
        self.set_key(self.__wj.get_value("key"))
        self.set_eth_name(self.__wj.get_value("eth_name"))
        self.__get_hn_status()
        if self.is_started():
            self.set_ssid(self.get_ssidname())

    def set_ssid(self, s):
        if s!= "":
            self.ssid = s

    def set_key(self, k):
        if k != "":
            self.key = k

    def set_eth_name(self, name):
        if name != "":
            self.eth_name = name

    def create_wifi(self, s = "", k = ""):
        self.set_ssid(s)
        self.set_key(k)
        self.__save_set()
        ret = subprocess.getstatusoutput("netsh wlan set hostednetwork mode=allow ssid={s} key={k}".format(s = self.ssid, k = self.key))
        self.__get_hn_status()
        return ret

    def start_wifi(self):
        ret = subprocess.getstatusoutput("netsh wlan start hostednetwork")
        self.__get_hn_status()
        self.__wd.close_connection_sharing(self.eth_name)
        self.__wd.start_connection_sharing(self.eth_name)
        return ret

    def stop_wifi(self):
        ret = subprocess.getstatusoutput("netsh wlan stop hostednetwork")
        self.__get_hn_status()
        return ret

    def close_wifi(self):
        ret = subprocess.getstatusoutput("netsh wlan set hostednetwork mode=disallow")
        self.__get_hn_status()
        self.__wd.close_connection_sharing(self.eth_name)
        return ret

    # return the status information of hostednetwork
    def show_wifi(self):
        return subprocess.getstatusoutput("netsh wlan show hostednetwork")

    # get all connections that may be shared
    def get_connections(self):
        ret = self.__wd.get_connections()
        if(True == ret[0]):
            return ret[2]
        else:
            return None

    # parse the status information of hostednetwork stored in self.hn_status
    def __get_hn_status(self):
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
    def __save_set(self):
        self.__wj.put_value("ssid", self.ssid)
        self.__wj.put_value("key", self.key)

    #===========================================================================
    # functions below only for windows in Chinese Lauguage
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
    print(ws.eth_name)
    print(ws.get_connections())
    print(ws.is_started())
    print(ws.get_user_num())
    print(ws.get_ssidname())
    print(ws.hn_status)
