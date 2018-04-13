#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WifiShare module used in windows
:author:
    yehuohan, 550034086@qq.com, yehuohan@gmail.com
"""

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

class JsonBase:
    """ JsonBase class.
    For writing and reading json-format file.
    """

    def __init__(self, filename):
        """ init JsonBase
        :Parameters:
            - filename: json-file's name
        """
        self.__filename = filename
        self.cf = None

    def is_json_exist(self):
        """ report json-file exist or not
        :Returns:
            existence of json file
        """
        return os.path.exists(self.__filename)

    def make_default(self, settings = {}):
        """ create default json-file
        :Parameters:
            - settings: default content of json-file
        """
        with open(self.__filename, "w", encoding="utf-8") as dump_f:
            json.dump(settings, dump_f)

    def open_json(self):
        """ read json-file """
        with open(self.__filename, "r", encoding="utf-8") as json_f:
            self.cf = json.load(json_f)

    def get_kv(self, key):
        """ get key-value
        :Parameters:
            - key: get the value response to key
        :Returns:
            value response to key
        """
        return self.cf[key]

    def put_kv(self, key, value):
        """ put key-value
        :Parameters:
            - key,value: write the key-value to json-file
        """
        self.cf[key] = value

    def write_json(self):
        """ write json """
        with open(self.__filename, "w", encoding="utf-8") as dump_f:
            json.dump(self.cf, dump_f)

class WsJson(JsonBase):
    """ WsJson class.
    class inheriting from JsonBase as setting of WifiShare class and pwshare.
    """

    # default settings value
    cf_defalut = {
        'pws.json': [
            'WifiShare',
            'Gui-qt',
            'Gui-tk'
        ],
        'WifiShare': {
            'ssid'     : "ubuntu",
            'key'      : "uuuuuuuu",
            'eth_name' : "以太网"
        },
        'Gui-qt': {
            'showpw'   : "True",
            'language' : "lang\\chinese.qm"
        },
        'Gui-tk': {}
    }

    def __init__(self, index_key):
        """ init WsJson
        :Parameters:
            - index_key: the main-key in json-file
        """
        self.__main_key = index_key     # main key in json-file
        self.__filename = "pws.json"    # filename of json-file
        super(WsJson, self).__init__(self.__filename)
        if super().is_json_exist() == False:
            super().make_default(self.cf_defalut)
        super().open_json()

    def get_value(self, key):
        """ get key-value in main_key
        :Parameters:
            - key: get the value response to key
        :Returns:
            the value response to key
        """
        return self.cf[self.__main_key][key]

    def put_value(self, key, value):
        """ put key-value in main_key
        :Parameters:
            - key,value: write key-value to the json-file
        """
        self.cf[self.__main_key][key] = value
        super().write_json()

class WsDll:
    """ WsDll class
    access ws-dll's funtions

    the return value of functions below in this format
    - format       : return (bool, function-ret, user-args)
    - bool         : Report function is execute successful or not
    - function-ret : Value function return, who's meanings can be found in dll's header-file
    - user-args    : What user expect function return. May more than one
    """

    def __init__(self, path = "ws.dll"):
        """ init WsDll
        :Parameters:
            - path: the path of ws.dll
        """
        self.__wsdll = ctypes.windll.LoadLibrary(path)

    def start_connection_sharing(self, eth_name):
        """ start connection sharing of ethernet and hostednetwork
        :Parameters:
            - eth_name: 将要共享网络连接的名称
        :Returns:
            返回一个元组tuple(flg, ret)
            - flg: 函数是否执行成功
            - ret: 函数返回值，即ws.dll接口的返回值
        """
        name_p = ctypes.c_wchar_p()
        name_p.value = eth_name;
        ret = self.__wsdll.ws_enable_sharing(name_p)
        if(0 == ret):
            return (True, ret)
        else:
            return (False, ret)

    def close_connection_sharing(self, eth_name):
        """ close connection sharing of ethernet and hostednetwork
        :Parameters:
            -eth_name: 共享网络连接的名称
        :Returns:
            返回一个元组tuple(flg, ret)
            - flg: 函数是否执行成功
            - ret: 函数返回值，即ws.dll接口的返回值
        """
        name_p = ctypes.c_wchar_p()
        name_p.value = eth_name;
        ret = self.__wsdll.ws_disable_sharing(name_p)
        if(0 == ret):
            return (True, ret)
        else:
            return (False, ret)

    def get_connections(self):
        """ get all connections's name to choose eth_name
        :Returns:
            返回一个元组tuple(flg, ret, cons)
            - flg: 函数是否执行成功
            - ret: 函数返回值，即ws.dll接口的返回值
            - cons: 所有连接名称列表(如果函数执行正确)
        """
        ret = ctypes.c_int()
        self.__wsdll.ws_py_get_connections.restype = ctypes.py_object
        cons = self.__wsdll.ws_py_get_connections(ctypes.byref(ret))
        if(0 == ret.value):
            # return result if get connections successful
            return (True, ret.value, cons)
        else:
            return (False, ret.value)

    def is_support_connection_sharing(self):
        """ report whether the operating-system supporting connection sharing
        :Returns:
            返回一个元组tuple(flg1, ret, flg2)
            - flg1: 函数是否执行成功
            - ret: 函数返回值，即ws.dll接口的返回值
            - flg2: 是否支持网络连接共享
        """
        flg = ctypes.c_bool()
        ret = self.__wsdll.ws_support_connection_sharing(ctypes.byref(flg))
        if(0 == ret):
            # flg is meaningful when function is executed successful
            return (True, ret, bool(flg.value))
        else:
            return (False, ret)

class WifiShare:
    """ WifiShare class.
    WifiShare manage wifi-setting, wifi-starting, wifi-closing, network-connection
    sharing, and json-setting.
    """

    def __init__(self):
        self.__wj = WsJson("WifiShare")
        self.__wd = WsDll("ws.dll")
        self.hn_status = {}
        self.ssid = None
        self.key = None
        self.eth_name = None # the name of the network-connection to be shared

        self.set_ssid(self.__wj.get_value("ssid"))
        self.set_key(self.__wj.get_value("key"))
        self.set_eth_name(self.__wj.get_value("eth_name"))
        self.__get_hn_status()
        if self.is_started():
            self.set_ssid(self.get_ssidname())

    def set_ssid(self, s):
        """ set ssid
        :Parameters:
            - s: name of wifi
        """
        if s!= "":
            self.ssid = s

    def set_key(self, k):
        """ set key
        :Parameters:
            - k: just the password of wifi
        """
        if k != "":
            self.key = k

    def set_eth_name(self, name):
        """ set network-connection name to self.eth_name
        :Parameters:
            - name: network-connection's name
        """
        if name != "":
            self.eth_name = name

    def create_wifi(self, s = "", k = ""):
        """ set wifi's ssid and key and then create wifi
        :Parameters:
            - s: ssid
            - k: key
        :Returns:
            return the status of command "netsh"
        """
        self.set_ssid(s)
        self.set_key(k)
        # save ssid and key to json in every creating-wifi time
        self.__wj.put_value("ssid", self.ssid)
        self.__wj.put_value("key", self.key)
        ret = subprocess.getstatusoutput("netsh wlan set hostednetwork mode=allow ssid={s} key={k}".format(s = self.ssid, k = self.key))
        self.__get_hn_status()
        return ret

    def start_wifi(self):
        """ start wifi
        create_wifi must be called before calling start_wifi

        :Returns:
            return the status of command "netsh"
        """
        ret = subprocess.getstatusoutput("netsh wlan start hostednetwork")
        self.__get_hn_status()
        self.__wd.close_connection_sharing(self.eth_name)
        self.__wd.start_connection_sharing(self.eth_name)
        # save eth_name to json in every sharing time
        self.__wj.put_value("eth_name", self.eth_name)
        return ret

    def stop_wifi(self):
        """ stop wifi
        wifi can be started again by calling start_wifi after stop_wifi

        :Returns:
            return the status of command "netsh"
        """
        ret = subprocess.getstatusoutput("netsh wlan stop hostednetwork")
        self.__get_hn_status()
        return ret

    def close_wifi(self):
        """ close wifi
        create_wifi have to be called again when you want to start wifi again

        :Returns:
            return the status of command "netsh"
        """
        ret = subprocess.getstatusoutput("netsh wlan set hostednetwork mode=disallow")
        self.__get_hn_status()
        self.__wd.close_connection_sharing(self.eth_name)
        return ret

    def show_wifi(self):
        """ return the status information of hostednetwork

        :Returns:
            return the status of command "netsh"
        """
        return subprocess.getstatusoutput("netsh wlan show hostednetwork")

    def get_connections(self):
        """ get all connections that may be shared
        :Returns:
            list of connection's name
        """
        ret = self.__wd.get_connections()
        if(True == ret[0]):
            return ret[2]
        else:
            return None

    def __get_hn_status(self):
        """ parse the status information of hostednetwork stored in self.hn_status
        :Returns:
            return the flag that function is executed successful or not
        """
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

    def is_started(self):
        """ chack if wifi si started
        :Returns:
            report wifi is started of not
        """
        if self.hn_status["状态"] == "已启动":
            return True
        else:
            return False

    def get_ssidname(self):
        """ get ssid name if wifi is already started
        :Returns:
            ssid of wifi
        """
        if self.is_started():
            return self.hn_status["SSID名称"].replace('“', "").replace('”', "")

    def get_user_num(self):
        """ get user(client) number
        :Returns:
            the number of user in using wifi
        """
        self.__get_hn_status()      # update user-num first
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
