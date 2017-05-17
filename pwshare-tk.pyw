

#===============================================================================
# file   : pwshare-gui
# brief  : python wifi share with tk-gui in windows
# e-mail : 550034086@qq.com, yehuohan@gmail.com
# author : yehuohan
#===============================================================================


#===============================================================================
# import
#===============================================================================
import sys
import tkinter as tk
from pyws import WifiShare

#===============================================================================
# MiniWS class : mini wifi share gui-program
#===============================================================================
class MiniWS():
    # wifi share module
    __ws = WifiShare()

    # main windows
    __mw = None
    __btn_start = None
    __lbl_msg = None

    # ui font
    __font = ("Consolas", 12)

    # ssid and key
    __ssid = None
    __key = None

    # message
    __msg = {"R":"Ready(in Admin)", "S":"Started Wifi", "C":"Closed Wifi"}

    def __init__(self):
        self.__mw = tk.Tk()
        self.__mw.title("MiniWS")
        self.__mw.geometry("280x210")
        self.__mw.resizable(width = False, height = True)
        self.init_ui()

    # init ui of main window
    def init_ui(self):
        # StringVar
        self.__ssid = tk.StringVar()
        self.__key = tk.StringVar()
        self.__ssid.set(self.__ws.ssid)
        self.__key.set(self.__ws.key)
        # label
        lbl_ssid = tk.Label(self.__mw, text = "SSID : ", font = self.__font)
        lbl_key = tk.Label(self.__mw, text = "KEY : ", font = self.__font)
        self.__lbl_msg = tk.Label(self.__mw, text = self.__msg["R"], font = self.__font, bg = "lightblue", width = 29, height = 2)
        # Entry
        ent_ssid = tk.Entry(self.__mw, textvariable = self.__ssid, font = self.__font)
        ent_key = tk.Entry(self.__mw, textvariable = self.__key, font = self.__font)
        # Button
        self.__btn_start = tk.Button(self.__mw, text = "Start", command = self.start_wifi, font = self.__font)
        btn_close = tk.Button(self.__mw, text = "Close", command = self.close_wifi, font = self.__font)
        # grid
        lbl_ssid.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "nes")
        lbl_key.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "nes")
        ent_ssid.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "nesw")
        ent_key.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = "nesw")
        self.__btn_start.grid(row = 2, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = "nesw")
        btn_close.grid(row = 3, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = "nesw")
        self.__lbl_msg.grid(row = 4, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = "w")

    def start_wifi(self):
        self.__ws.create_wifi(s = self.__ssid.get(), k = self.__key.get())
        self.__ws.start_wifi()
        self.__btn_start["text"] = "ReStart"
        self.__btn_start["command"] = self.restart_wifi
        self.__lbl_msg["text"] = self.__msg["S"]

    def restart_wifi(self):
        self.__ws.close_wifi()
        self.__ws.create_wifi(s = self.__ssid.get(), k = self.__key.get())
        self.__ws.start_wifi()

    def close_wifi(self):
        self.__ws.close_wifi()
        self.__btn_start["text"] = "Start"
        self.__btn_start["command"] = self.start_wifi
        self.__lbl_msg["text"] = self.__msg["C"]

    # execute main-loop
    def exec(self):
        self.__mw.mainloop()


#===============================================================================
# Main-Loop
#===============================================================================

if __name__ == "__main__":
    mws = MiniWS()
    mws.exec()
