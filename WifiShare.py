
#===============================================================================
# file   : WifiShare.py
# brief  : WifiShare module used in windows
# e-mail : 550034086@qq.com, yehuohan@gmail.com
# author : yehuohan
#===============================================================================


#===============================================================================
# import
#===============================================================================
import subprocess

#===============================================================================
# WifiShare class
#===============================================================================
class WifiShare:
    ssid = "ubuntu"
    key = "uuuuuuuu"

    def set_ssid(self, s):
        if s!= "":
            self.ssid = s

    def set_key(self, k):
        if k != "":
            self.key = k

    def create_wifi(self, s = "", k = ""):
        self.set_ssid(s)
        self.set_key(k)
        return subprocess.getstatusoutput("netsh wlan set hostednetwork mode=allow ssid={s} key={k}".format(s = self.ssid, k = self.key))

    def start_wifi(self):
        return subprocess.getstatusoutput("netsh wlan start hostednetwork")

    def stop_wifi(self):
        return subprocess.getstatusoutput("netsh wlan stop hostednetwork")

    def close_wifi(self):
        return subprocess.getstatusoutput("netsh wlan set hostednetwork mode=disallow")

