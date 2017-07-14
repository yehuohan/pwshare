
## @file pws.py
#  @brief WifiShare module used in windows
#  
#  @date
#  @version
#  @author yehuohan, 550034086@qq.com, yehuohan@gmail.com
#  @copyright

#===============================================================================
# import
#===============================================================================
import os
import subprocess
import json
import ctypes


#===============================================================================
# Class
#===============================================================================

## @defgroup PWS wifi-share python module
#  
#  @{

## @brief JsonBase class
# 
#  For writing and reading json-format file
class JsonBase:
    __filename = None
    cf = None

    ## @brief init of JsonBase
    # 
    #  @param filename: json-file's name
    def __init__(self, filename):
        self.__filename = filename

    ## @brief report json-file exist or not
    #
    #  @return existence of json file
    def is_json_exist(self):
        return os.path.exists(self.__filename)

    ## @brief create default json-file
    #
    #  @param settings: default content of json-file
    #  @return
    #  @retval
    def make_default(self, settings = {}):
        with open(self.__filename, "w", encoding="utf-8") as dump_f:
            json.dump(settings, dump_f)

    ## @brief read json-file
    #
    #  @param
    #  @return
    #  @retval
    def open_json(self):
        with open(self.__filename, "r", encoding="utf-8") as json_f:
            self.cf = json.load(json_f)

    ## @brief get key-value 
    #
    #  @param key: get the value response to key
    #  @return value response to key
    #  @retval
    def get_kv(self, key):
        return self.cf[key]

    ## @brief put key-value
    #
    #  @param key-value: write the key-value to json-file
    #  @return
    #  @retval
    def put_kv(self, key, value):
        self.cf[key] = value

    ## @brief write json
    #
    #  @param
    #  @return
    #  @retval
    def write_json(self):
        with open(self.__filename, "w", encoding="utf-8") as dump_f:
            json.dump(self.cf, dump_f)


## @brief WsJson class
#
#  class inheriting from JsonBase as setting of WifiShare class and pwshare
class WsJson(JsonBase):
    ## filename of json-file
    __filename = "pws.json"

    ## main key in json-file
    __main_key = None 

    ## default settings value
    cf_defalut = {
        "pws.json": [
            "WifiShare",
            "Gui-qt",
            "Gui-tk"
        ],
        "WifiShare": {
            "ssid"     : "ubuntu",
            "key"      : "uuuuuuuu",
            "eth_name" : "以太网"
        },
        "Gui-qt": {
            "showpw"   : "True",
            "language" : "lang\\chinese.qm"
        },
        "Gui-tk": {}
    }

    ## @brief init of WsJson
    # 
    #  @param index_key: the main-key in json-file
    #  @return
    #  @retval
    def __init__(self, index_key):
        self.__main_key = index_key
        super(WsJson, self).__init__(self.__filename)
        if super().is_json_exist() == False:
            super().make_default(self.cf_defalut)
        super().open_json()

    ## @brief get key-value in main_key
    # 
    #  @param key: get the value response to key
    #  @return the value response to key
    def get_value(self, key):
        return self.cf[self.__main_key][key]

    ## @brief put key-value in main_key
    # 
    #  @param key-value: write key-value to the json-file
    def put_value(self, key, value):
        self.cf[self.__main_key][key] = value
        super().write_json()


## @brief WsDll class 
#
#  access ws-dll's funtions
class WsDll:
    __wsdll = None

    ## @brief init of WsDll
    # 
    #  @param path: the path of ws.dll
    #  @return
    #  @retval
    def __init__(self, path = "ws.dll"):
        self.__wsdll = ctypes.windll.LoadLibrary(path)

    #===========================================================================
    # the return value of functions below in this format
    # format       : return (bool, function-ret, user-args)
    # bool         : Report function is execute successful or not
    # function-ret : Value function return, who's meanings can be found in dll's header-file
    # user-args    : What user expect function return. May more than one
    #===========================================================================

    ## @brief start connection sharing of ethernet and hostednetwork
    # 
    #  @param eth_name: 将要共享网络连接的名称
    #  @return 返回一个元组tuple(flg, ret)
    #  @retval flg: 函数是否执行成功
    #  @retval ret: 函数返回值，即ws.dll接口的返回值
    def start_connection_sharing(self, eth_name):
        name_p = ctypes.c_wchar_p()
        name_p.value = eth_name;
        ret = self.__wsdll.ws_enable_sharing(name_p)
        if(0 == ret):
            return (True, ret)
        else:
            return (False, ret)

    ## @brief close connection sharing of ethernet and hostednetwork
    # 
    #  @param eth_name: 共享网络连接的名称
    #  @return 返回一个元组tuple(flg, ret)
    #  @retval flg: 函数是否执行成功
    #  @retval ret: 函数返回值，即ws.dll接口的返回值
    def close_connection_sharing(self, eth_name):
        name_p = ctypes.c_wchar_p()
        name_p.value = eth_name;
        ret = self.__wsdll.ws_disable_sharing(name_p)
        if(0 == ret):
            return (True, ret)
        else:
            return (False, ret)

    ## @brief get all connections's name to choose eth_name
    # 
    #  @return 返回一个元组tuple(flg, ret, cons)
    #  @retval flg: 函数是否执行成功
    #  @retval ret: 函数返回值，即ws.dll接口的返回值
    #  @retval cons: 所有连接名称列表(如果函数执行正确)
    def get_connections(self):
        ret = ctypes.c_int()
        self.__wsdll.ws_py_get_connections.restype = ctypes.py_object
        cons = self.__wsdll.ws_py_get_connections(ctypes.byref(ret))
        if(0 == ret.value):
            # return result if get connections successful
            return (True, ret.value, cons)
        else:
            return (False, ret.value)

    ## @brief report whether the operating-system supporting connection sharing
    # 
    #  @return 返回一个元组tuple(flg1, ret, flg2)
    #  @retval flg1: 函数是否执行成功
    #  @retval ret: 函数返回值，即ws.dll接口的返回值
    #  @retval flg2: 是否支持网络连接共享
    def is_support_connection_sharing(self):
        flg = ctypes.c_bool()
        ret = self.__wsdll.ws_support_connection_sharing(ctypes.byref(flg))
        if(0 == ret):
            # flg is meaningful when function is executed successful
            return (True, ret, bool(flg.value))
        else:
            return (False, ret)


## @brief WifiShare class
#
#  WifiShare manage wifi-setting, wifi-starting, wifi-closing, network-connection
#  sharing, and json-setting.
class WifiShare:
    __wj = WsJson("WifiShare")
    __wd = WsDll("ws.dll")

    ## @name hosted-network's status, ssid and key
    #  @{
    hn_status = {}
    ssid = None
    key = None
    ## @}

    ## the name of the network-connection to be shared
    eth_name = None

    def __init__(self):
        self.set_ssid(self.__wj.get_value("ssid"))
        self.set_key(self.__wj.get_value("key"))
        self.set_eth_name(self.__wj.get_value("eth_name"))
        self.__get_hn_status()
        if self.is_started():
            self.set_ssid(self.get_ssidname())

    ## @brief set ssid
    # 
    #  @param s: name of wifi
    #  @return
    #  @retval
    def set_ssid(self, s):
        if s!= "":
            self.ssid = s

    ## @brief set key
    # 
    #  @param k: just the password of wifi
    #  @return
    #  @retval
    def set_key(self, k):
        if k != "":
            self.key = k

    ## @brief set network-connection name to self.eth_name
    # 
    #  @param name: network-connection's name
    #  @return
    #  @retval
    def set_eth_name(self, name):
        if name != "":
            self.eth_name = name

    ## @brief set wifi's ssid and key and then create wifi
    # 
    #  @param s: ssid
    #  @param k: key
    #  @return return the status of command "netsh"
    #  @retval
    def create_wifi(self, s = "", k = ""):
        self.set_ssid(s)
        self.set_key(k)
        # save ssid and key to json in every creating-wifi time
        self.__wj.put_value("ssid", self.ssid)
        self.__wj.put_value("key", self.key)
        ret = subprocess.getstatusoutput("netsh wlan set hostednetwork mode=allow ssid={s} key={k}".format(s = self.ssid, k = self.key))
        self.__get_hn_status()
        return ret

    ## @brief start wifi
    # 
    #  create_wifi must be called before calling start_wifi
    #
    #  @return return the status of command "netsh"
    #  @retval
    def start_wifi(self):
        ret = subprocess.getstatusoutput("netsh wlan start hostednetwork")
        self.__get_hn_status()
        self.__wd.close_connection_sharing(self.eth_name)
        self.__wd.start_connection_sharing(self.eth_name)
        # save eth_name to json in every sharing time
        self.__wj.put_value("eth_name", self.eth_name)
        return ret

    ## @brief stop wifi
    # 
    #  wifi can be started again by calling start_wifi after stop_wifi
    #
    #  @return return the status of command "netsh"
    #  @retval
    def stop_wifi(self):
        ret = subprocess.getstatusoutput("netsh wlan stop hostednetwork")
        self.__get_hn_status()
        return ret

    ## @brief close wifi
    # 
    #  create_wifi have to be called again when you want to start wifi again
    #
    #  @return return the status of command "netsh"
    def close_wifi(self):
        ret = subprocess.getstatusoutput("netsh wlan set hostednetwork mode=disallow")
        self.__get_hn_status()
        self.__wd.close_connection_sharing(self.eth_name)
        return ret

    ## @brief return the status information of hostednetwork
    # 
    #  @return return the status of command "netsh"
    #  @retval
    def show_wifi(self):
        return subprocess.getstatusoutput("netsh wlan show hostednetwork")

    ## @brief get all connections that may be shared
    # 
    #  @return list of connection's name
    #  @retval
    def get_connections(self):
        ret = self.__wd.get_connections()
        if(True == ret[0]):
            return ret[2]
        else:
            return None

    ## @brief parse the status information of hostednetwork stored in self.hn_status
    # 
    #  @return return the flag that function is executed successful or not
    #  @retval
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


    #===========================================================================
    # functions below only for windows in Chinese Lauguage
    #===========================================================================

    ## @brief check if wifi is started
    # 
    #  @return report wifi is started of not
    #  @retval
    def is_started(self):
        if self.hn_status["状态"] == "已启动":
            return True
        else:
            return False

    ## @brief get ssid name if wifi is already started
    # 
    #  @return ssid of wifi
    #  @retval
    def get_ssidname(self):
        if self.is_started():
            return self.hn_status["SSID名称"].replace('“', "").replace('”', "")

    ## @brief get user(client) number
    # 
    #  @param None
    #  @return the number of user in using wifi
    #  @retval
    def get_user_num(self):
        self.__get_hn_status()      # update user-num first
        if self.is_started():
            return self.hn_status["客户端数"]


## @}

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
