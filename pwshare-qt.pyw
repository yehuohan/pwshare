#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PwShare
PwShare是基于Python和C++而实现Wifi热点的工具。
特点
 - 使用python实现界面(qt5)和逻辑。
 - 使用C++开发实现Wifi连接共享的dll链接库。

:author:
    - yehuohan, 550034086@qq.com, yehuohan@gmail.com
"""


#===============================================================================
# import
#===============================================================================
import sys
import glob
import PyQt5.Qt as qt
import pwshare_rc
from pws import WifiShare, WsJson


#===============================================================================
# Class
#===============================================================================

class ui_pwshare(qt.QObject):
    """ ui_pwhare class
    ui of pwhare class
    """

    def setup_ui(self, dlg):
        """ set ui to one widget
        :Parameters:
            - dlg: the widget to setup_ui
        """
        self.setParent(dlg)
        # Dialog setting
        dlg.setFont(qt.QFont("Cousine", 11))
        dlg.setWindowIcon(qt.QIcon(":/res/res/dlg_wifi.png"))
        dlg.setWindowFlags(qt.Qt.WindowMinimizeButtonHint | qt.Qt.WindowCloseButtonHint)
        dlg.resize(350, 390)
        dlg.setFixedWidth(300)

        # create ctrl
        self.lbl_ssid = qt.QLabel(dlg)
        self.lbl_key = qt.QLabel(dlg)
        self.txt_ssid = qt.QLineEdit(dlg)
        self.txt_key = qt.QLineEdit(dlg)
        self.act_eye = qt.QAction(dlg)
        self.lbl_connection = qt.QLabel(dlg)
        self.cmb_connection = qt.QComboBox(dlg)
        self.lbl_lang = qt.QLabel(dlg)
        self.cmb_lang = qt.QComboBox(dlg)
        self.btn_start = qt.QPushButton(dlg)
        self.txt_status = qt.QPlainTextEdit(dlg)

        # Size
        self.txt_ssid.setFixedHeight(32)
        self.txt_key.setFixedHeight(32)
        self.cmb_connection.setFixedHeight(32)
        self.cmb_lang.setFixedHeight(32)
        self.btn_start.setFixedHeight(32)

        # StyleSheet
        self.txt_ssid.setStyleSheet(
                """QLineEdit{
                    border-width: 1px;
                    border-radius: 5px;
                    border:1px solid gray;
                    color: black;
                }
                QLineEdit:hover{
                    border:1px solid rgb(70, 200, 50);
                }""")
        self.txt_key.addAction(self.act_eye, qt.QLineEdit.TrailingPosition)
        self.txt_key.setClearButtonEnabled(True)
        self.txt_key.setStyleSheet(self.txt_ssid.styleSheet())
        self.act_eye.setCheckable(True)
        self.act_eye.toggled[bool].connect(self.toggle_eye_icon)
        self.txt_status.setReadOnly(True)
        self.txt_status.setStyleSheet(
                """
                background-color : rgb(200,200,200);
                color            : green;
                font-weight      : bold;
                """)

        # system tray-icon
        self.act_quit = qt.QAction(dlg)
        self.tray_menu = qt.QMenu(dlg)
        self.tray_menu.addAction(self.act_quit)
        self.tray_icon = qt.QSystemTrayIcon(qt.QIcon(":/res/res/dlg_wifi.png"), dlg)
        self.tray_icon.setVisible(True)
        self.tray_icon.setContextMenu(self.tray_menu)

        # set text of ctrl
        self.set_translator(dlg)

        # GridLayout setting
        self.grid = qt.QGridLayout(dlg)
        self.grid.addWidget(self.lbl_ssid, 0, 0)
        self.grid.addWidget(self.txt_ssid, 0, 1)
        self.grid.addWidget(self.lbl_key, 1, 0)
        self.grid.addWidget(self.txt_key, 1, 1)
        self.grid.addWidget(self.lbl_connection, 2, 0)
        self.grid.addWidget(self.cmb_connection, 2, 1)
        self.grid.addWidget(self.lbl_lang, 3, 0)
        self.grid.addWidget(self.cmb_lang, 3, 1)
        self.grid.addWidget(self.btn_start, 4, 0, 1, 2)
        self.grid.addWidget(self.txt_status, 5, 0, 1, 2)

    def set_translator(self, dlg):
        """ set text of all object
        :Parameters:
            - dlg: the widget of ui
        """
        dlg.setWindowTitle(self.tr("PyWifiShare"))
        self.txt_key.setPlaceholderText(self.tr("PassWord"))
        self.lbl_ssid.setText(self.tr("SSID:"))
        self.lbl_key.setText(self.tr("KEY:"))
        self.lbl_connection.setText(self.tr("CONN:"))
        self.lbl_lang.setText(self.tr("LANG:"))
        self.act_quit.setText(self.tr("Quit"))

    def set_btn_start_text(self, flg):
        """ set the text of pushbutton of btn_start according to flg
        :Parameters:
            - flg: True for "Close" and False for "Start"
        """
        if True == flg:
            self.btn_start.setText(self.tr("Close"))
        else:
            self.btn_start.setText(self.tr("Start"))

    @qt.pyqtSlot(bool)
    def toggle_eye_icon(self, flg):
        """ qt slot for toggling icon of password-eye
        :Parameters:
            - flg: True for show password and False for hide password
        """
        if True == flg:
            self.txt_key.setEchoMode(qt.QLineEdit.Normal)
            self.act_eye.setIcon(qt.QIcon(":/res/res/btn_eye_show.png"))
        else:
            self.txt_key.setEchoMode(qt.QLineEdit.Password)
            self.act_eye.setIcon(qt.QIcon(":/res/res/btn_eye_hide.png"))

class pwshare(qt.QDialog):
    """ pwshare class
    wifi share gui-program
    """

    def __init__(self, parent = None):
        super(pwshare, self).__init__(parent)
        self.ui = ui_pwshare()
        self.translator = qt.QTranslator()
        self.__ws = WifiShare()
        self.__wj = WsJson("Gui-qt")

        self.translator.load(self.__wj.get_value("language"))
        qt.qApp.installTranslator(self.translator)
        self.ui.setup_ui(self)
        self.__init_data()
        self.__create_connection()

    def __init_data(self):
        """ init data """
        # set ssid and key value
        self.ui.txt_ssid.setText(self.__ws.ssid)
        self.ui.txt_key.setText(self.__ws.key)
        # show password or not
        self.ui.act_eye.toggle()
        if self.__wj.get_value("showpw") == "True":
            self.ui.act_eye.setChecked(True)
        elif self.__wj.get_value("showpw") == "False":
            self.ui.act_eye.setChecked(False)
        # status information
        self.ui.txt_status.setPlainText(self.get_time()+self.tr("Ready(Must be Admin)\n"))
        if self.__ws.is_started():
            self.ui.txt_status.setPlainText(self.ui.txt_status.toPlainText()+self.get_time()+self.tr("Wifi is Not closed last time\n"))
        # language selection
        lang_list = glob.glob("lang/*.qm")
        for qm in lang_list:
            self.ui.cmb_lang.addItem(qm)
            if qm == self.__wj.get_value("language"):
                self.ui.cmb_lang.setCurrentText(qm)
        # ethernet connection
        conn_list = self.__ws.get_connections()
        for name in conn_list:
            self.ui.cmb_connection.addItem(name)
            if name == self.__ws.eth_name:
                self.ui.cmb_connection.setCurrentText(name)
        # start or close button
        self.ui.set_btn_start_text(self.__ws.is_started())

    def __create_connection(self):
        """ create connection """
        # start or close wifi
        if self.__ws.is_started():
            self.ui.btn_start.released.connect(self.close_wifi)
        else:
            self.ui.btn_start.released.connect(self.start_wifi)
        # show password
        self.ui.act_eye.toggled[bool].connect(self.save_showpw)
        # switch language
        self.ui.cmb_lang.currentTextChanged[str].connect(self.switch_lang)
        # switch connection
        self.ui.cmb_connection.currentTextChanged[str].connect(lambda name:self.__ws.set_eth_name(name))
        # tray-icon
        self.ui.tray_icon.activated[qt.QSystemTrayIcon.ActivationReason].connect(self.tray_icon_active)
        self.ui.act_quit.triggered.connect(lambda:self.close())

    @qt.pyqtSlot(qt.QSystemTrayIcon.ActivationReason)
    def tray_icon_active(self, reason):
        """ tray-icon activated slot """
        if reason == qt.QSystemTrayIcon.Trigger or reason == qt.QSystemTrayIcon.DoubleClick:
            self.showNormal()
            self.setFocus()

    @qt.pyqtSlot(str)
    def switch_lang(self, lang):
        """ switch language """
        self.translator.load(lang)
        qt.qApp.installTranslator(self.translator)
        self.ui.set_translator(self)
        self.ui.set_btn_start_text(self.__ws.is_started())
        self.__wj.put_value("language", lang)

    @qt.pyqtSlot()
    def start_wifi(self):
        """ create wifi with ssid and key """
        msg = self.get_time() + self.tr("Starting Wifi......\n")
        msg_error = self.get_time() + self.tr("Error: check Admin!\n")
        ret = self.__ws.create_wifi(s = self.ui.txt_ssid.text(), k = self.ui.txt_key.text())
        if 0 == ret[0]:
            # start the created wifi
            msg += self.get_time() + ret[1]
            ret = self.__ws.start_wifi()
            if 0 == ret[0]:
                # show message
                msg += self.get_time() + ret[1]
                msg += self.get_time() + self.tr("Wifi started\n")
                self.ui.txt_status.setPlainText(msg)
                self.ui.btn_start.released.disconnect(self.start_wifi)
                self.ui.btn_start.released.connect(self.close_wifi)
                self.ui.set_btn_start_text(True)
                return True
            else:
                msg_error += self.get_time() + ret[1]
        else:
            msg_error += self.get_time() + ret[1]
        # failed to create or start wifi
        self.ui.txt_status.setPlainText(msg_error)
        return False

    @qt.pyqtSlot()
    def close_wifi(self):
        msg = self.get_time() + self.tr("Closing Wifi......\n")
        msg_error = self.get_time() + self.tr("Error: check Admin!\n")
        ret = self.__ws.close_wifi()
        if 0 == ret[0]:
            msg += self.get_time() + ret[1]
            msg += self.get_time() + self.tr("Wifi closed\n")
            self.ui.txt_status.setPlainText(msg)
            self.ui.btn_start.released.disconnect(self.close_wifi)
            self.ui.btn_start.released.connect(self.start_wifi)
            self.ui.set_btn_start_text(False)
            return True
        else:
            msg_error += self.get_time() + ret[1]
        # failed to close wifi
        self.ui.txt_status.setPlainText(msg_error)
        return False

    def get_time(self):
        """ get current time """
        return "[" + qt.QTime.currentTime().toString() + "] "

    @qt.pyqtSlot(bool)
    def save_showpw(self, flg):
        """ save show-password """
        if flg:
            self.__wj.put_value("showpw", "True")
        else:
            self.__wj.put_value("showpw", "False")
        return True

    def changeEvent(self, event):
        """ change event: hide when minimized """
        if event.type() == qt.QEvent.WindowStateChange and self.isMinimized():
            self.hide()


if __name__ == "__main__":
    app = qt.QApplication(sys.argv)
    app.setStyle(qt.QStyleFactory.create("fusion"));
    ws = pwshare()
    ws.show()
    app.exec()

