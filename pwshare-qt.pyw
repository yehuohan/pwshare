
#===============================================================================
# file   : pwshare.pyw
# brief  : python wifi share with qt-gui in windows
# e-mail : 550034086@qq.com, yehuohan@gmail.com
# author : yehuohan
#===============================================================================

#===============================================================================
# import
#===============================================================================
import sys
import glob
import PyQt5.Qt as qt
import pwshare_rc
from pws import WifiShare, WsJson


#===============================================================================
# ui_pwshare class : ui of pwshare
#===============================================================================
class ui_pwshare(qt.QObject):
    def setup_ui(self, dlg):
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
        self.btn_eye = qt.QPushButton(dlg)
        self.lbl_connection = qt.QLabel(dlg)
        self.cmb_connection = qt.QComboBox(dlg)
        self.lbl_lang = qt.QLabel(dlg)
        self.cmb_lang = qt.QComboBox(dlg)
        self.btn_start = qt.QPushButton(dlg)
        self.txt_status = qt.QPlainTextEdit(dlg)

        # Size
        self.txt_ssid.setFixedHeight(32)
        self.txt_key.setFixedHeight(32)
        self.btn_eye.setFixedSize(32,32)
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
        self.txt_key.setClearButtonEnabled(True)
        self.txt_key.setStyleSheet(self.txt_ssid.styleSheet())
        self.btn_eye.setCheckable(True)
        self.btn_eye.setStyleSheet(
                """QPushButton{
                    border-radius : 6px;
                    border        : 2px outset rgb(180,180,180);
                    image         : url(:/res/res/btn_eye_hide.png);
                }
                QPushButton:pressed{
                    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0 #dadbde, stop: 1 #f6f7fa);
                }
                QPushButton:checked{
                    image        : url(:/res/res/btn_eye_show.png);
                    border-style : inset;
                }""")
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
        self.grid.addWidget(self.txt_ssid, 0, 1, 1, 2)
        self.grid.addWidget(self.lbl_key, 1, 0)
        self.grid.addWidget(self.txt_key, 1, 1)
        self.grid.addWidget(self.btn_eye, 1, 2)
        self.grid.addWidget(self.lbl_connection, 2, 0)
        self.grid.addWidget(self.cmb_connection, 2, 1, 1, 2)
        self.grid.addWidget(self.lbl_lang, 3, 0)
        self.grid.addWidget(self.cmb_lang, 3, 1, 1, 2)
        self.grid.addWidget(self.btn_start, 4, 0, 1, 3)
        self.grid.addWidget(self.txt_status, 5, 0, 1, 3)


    def set_translator(self, dlg):
        dlg.setWindowTitle(self.tr("PyWifiShare"))
        self.txt_key.setPlaceholderText(self.tr("PassWord"))
        self.lbl_ssid.setText(self.tr("SSID:"))
        self.lbl_key.setText(self.tr("KEY:"))
        self.lbl_connection.setText(self.tr("CONN:"))
        self.lbl_lang.setText(self.tr("LANG:"))
        self.act_quit.setText(self.tr("Quit"))

    def set_btn_start_text(self, flg):
        if True == flg:
            self.btn_start.setText(self.tr("Close"))
        else:
            self.btn_start.setText(self.tr("Start"))


#===============================================================================
# pwshare class : wifi share gui-program
#===============================================================================
class pwshare(qt.QDialog):
    ui = ui_pwshare()
    translator = qt.QTranslator()
    __ws = WifiShare()
    __wj = WsJson("Gui-qt")

    # initial
    def __init__(self, parent = None):
        super(pwshare, self).__init__(parent)
        self.translator.load(self.__wj.get_value("language"))
        qt.qApp.installTranslator(self.translator)
        self.ui.setup_ui(self)
        self.init_data()
        self.create_connection()

    def init_data(self):
        # set ssid and key value
        self.ui.txt_ssid.setText(self.__ws.ssid)
        self.ui.txt_key.setText(self.__ws.key)
        # show password or not
        if self.__wj.get_value("showpw") == "True":
            self.ui.btn_eye.setChecked(True)
            self.ui.txt_key.setEchoMode(qt.QLineEdit.Normal) 
        elif self.__wj.get_value("showpw") == "False":
            self.ui.btn_eye.setChecked(False)
            self.ui.txt_key.setEchoMode(qt.QLineEdit.Password)
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

    def create_connection(self):
        # start or close wifi
        if self.__ws.is_started():
            self.ui.btn_start.released.connect(self.close_wifi)
        else:
            self.ui.btn_start.released.connect(self.start_wifi)
        # show password
        toggle_echomode = lambda flg : self.ui.txt_key.setEchoMode(qt.QLineEdit.Normal) if flg else self.ui.txt_key.setEchoMode(qt.QLineEdit.Password)
        self.ui.btn_eye.toggled[bool].connect(
                lambda flg : self.save_showpw(flg) and toggle_echomode(flg))
        # switch language
        self.ui.cmb_lang.currentTextChanged[str].connect(self.switch_lang)
        # switch connection
        self.ui.cmb_connection.currentTextChanged[str].connect(lambda name:self.__ws.set_eth_name(name))
        # tray-icon
        self.ui.tray_icon.activated[qt.QSystemTrayIcon.ActivationReason].connect(self.tray_icon_active)
        self.ui.act_quit.triggered.connect(lambda:self.close())

    # tray-icon activated slot
    @qt.pyqtSlot(qt.QSystemTrayIcon.ActivationReason)
    def tray_icon_active(self, reason):
        if reason == qt.QSystemTrayIcon.Trigger or reason == qt.QSystemTrayIcon.DoubleClick:
            self.showNormal()
            self.setFocus()

    # switch language
    @qt.pyqtSlot(str)
    def switch_lang(self, lang):
        self.translator.load(lang)
        qt.qApp.installTranslator(self.translator)
        self.ui.set_translator(self)
        self.ui.set_btn_start_text(self.__ws.is_started())
        self.__wj.put_value("language", lang)

    @qt.pyqtSlot()
    def start_wifi(self):
        # create wifi with ssid and key
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

    # get current time
    def get_time(self):
        return "[" + qt.QTime.currentTime().toString() + "] "

    # save show-password
    def save_showpw(self, flg):
        if flg:
            self.__wj.put_value("showpw", "True")
        else:
            self.__wj.put_value("showpw", "False")
        return True 

    # change event: hide when minimized
    def changeEvent(self, event):
        if event.type() == qt.QEvent.WindowStateChange and self.isMinimized():
            self.hide()


#===============================================================================
# main-loop
#===============================================================================
if __name__ == "__main__":
    app = qt.QApplication(sys.argv)
    app.setStyle(qt.QStyleFactory.create("fusion"));
    ws = pwshare()
    ws.show()
    app.exec()

