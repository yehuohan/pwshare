#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
python wifi share in windows
:author:
    yehuohan, 550034086@qq.com, yehuohan@gmail.com
"""

#===============================================================================
# import
#===============================================================================
import sys
import cmd
import subprocess
from pws import WifiShare


class WSCLI(cmd.Cmd):
    """ WSCLI class.
    wifi share command-line interface
    """
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "Python@Wifi-Share > "           # command prompt

    # "help help" or "!help" call this function when no override for do_help
    def help_help(self):             
        print("Print help")

    # quit the main-loop of CLI
    def do_quit(self, arg):
        return True

    # run system command such as "!cmd", "!dir", etc.
    def do_shell(self, arg):
        subshell = subprocess.Popen(arg, shell = True, stdin = None, stdout=None)
        subshell.communicate()
        subshell.terminate()

    #===========================================================================
    # class user command and variable
    #===========================================================================

    __ws = WifiShare()

    # wifi share command: set
    def do_set(self, arg):
        if arg != "":
            # split the arg to search "ssid" and "key"
            if arg.find("=") != -1:
                ssid = ""
                key = ""
                for i in arg.split():
                    args = i.split("=")
                    if args[0] == "ssid":
                        ssid = args[1]
                    elif args[0] == "key":
                        key = args[1]
                self.__ws.create_wifi(ssid, key)
        else:
            self.__ws.create_wifi(arg)

    # wifi share command: wifi
    def do_wifi(self, arg):
        if arg == "start":
            self.__ws.start_wifi()
        elif arg == "stop":
            self.__ws.stop_wifi()
        elif arg == "close":
            self.__ws.close_wifi()
        else:
            print("Unkown command:{}".format(arg))

    # help <cmd>
    def do_help(self, arg):
        if arg == "set":
            print("""
set [ssid=<name>] [key=<code>]
    - ssid : set the wifi name
    - key  : set the wifi key
            """)
        elif arg == "wifi":
            print("""
wifi <mode>:
    - mode 'start'   : start the wifi had set
    - mode 'stop'    : stop the wifi but can be started again
    - mode 'close'   : close the wifi and need to set again
            """)
        elif arg == "quit":
            print("""
quit
    : quit the pwshare program
            """)
        elif arg == "":
            print("""
Command:
    - set [ssid=<ssid>] [ssid=<key>]
    - wifi <mode>
    - quit
            """)



if __name__ == "__main__":
    wscli = WSCLI()
    try:
        wscli.cmdloop("Command-Line Interface")
    except KeyboardInterrupt as e:
        print("Exit")
