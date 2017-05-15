
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


#===============================================================================
# WifiShare class
#===============================================================================
class WifiShare:
    ssid = "ubuntu"
    key = "uuuuuuuu"

    def print_wifi(self):
        print(" wifi ssid : " + self.ssid)
        print(" wifi key  : " + self.key)
        print("")

    def set_ssid(self, s):
        if s!= "":
            self.ssid = s

    def set_key(self, k):
        if k != "":
            self.key = k

    def create_wifi(self, s = "", k = ""):
        os.system("netsh wlan set hostednetwork mode=allow ssid={s} key={k}".format(s = self.ssid, k = self.key))
        self.set_ssid(s)
        self.set_key(k)

    def start_wifi(self):
        os.system("netsh wlan start hostednetwork")

    def stop_wifi(self):
        os.system("netsh wlan stop hostednetwork")

    def restart_wifi(self):
        self.close_wifi()
        self.create_wifi()
        self.start_wifi()

    def close_wifi(self):
        os.system("netsh wlan set hostednetwork mode=disallow")

