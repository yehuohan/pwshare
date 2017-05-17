
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
import PyQt5.Qt as qt
from WifiShare import WifiShare

#===============================================================================
# MiniWS class : mini wifi share gui-program
#===============================================================================
class MiniWS(qt.QDialog):
    # qt ctrl
    txt_ssid = None
    txt_key = None
    btn_start = None
    lbl_status = None
    status_code = ("Closed", "Started")
    status = status_code[0]

    # Wifi-Share class
    __ws = WifiShare()

    def __init__(self, parent = None):
        super(MiniWS, self).__init__(parent)
        # init MiniWS
        self.setFont(qt.QFont("Cousine", 11))
        #self.setFont(qt.QFont("Courier New", 11))
        self.setWindowTitle(self.tr("Mini WifiShare"))
        self.resize(300, 370)
        self.setFixedWidth(280)
        self.init_ui()

    # init ui of main window
    def init_ui(self):
        # create ctrl
        lbl_ssid = qt.QLabel(self.tr("SSID: "), self)
        lbl_key = qt.QLabel(self.tr("KEY: "), self)
        self.lbl_status = qt.QLabel(self.get_time()+self.tr("Ready(Must be Admin)"),self)
        self.lbl_status.setAlignment(qt.Qt.AlignLeft) 
        self.lbl_status.setWordWrap(True)
        self.lbl_status.setStyleSheet("""
                                    color: darkred;
                                    background-color: lightblue
                                    """)
        self.txt_ssid = qt.QLineEdit(self)
        self.txt_key = qt.QLineEdit(self)
        self.txt_ssid.setText(self.__ws.ssid)
        self.txt_key.setText(self.__ws.key)
        self.btn_start = qt.QPushButton(self.tr("Start"), self)
        btn_close = qt.QPushButton(self.tr("Close"), self)
        chk_showpw = qt.QCheckBox(self.tr("Show Passwd"), self)
        chk_showpw.setChecked(True)
        # grid-layout
        grid = qt.QGridLayout(self)
        grid.addWidget(lbl_ssid, 0, 0)
        grid.addWidget(lbl_key, 1, 0)
        grid.addWidget(self.txt_ssid, 0, 1)
        grid.addWidget(self.txt_key, 1, 1)
        grid.addWidget(chk_showpw, 2, 0, 1, 2)
        grid.addWidget(self.btn_start, 3, 0, 1, 2)
        grid.addWidget(btn_close, 4, 0, 1, 2)
        grid.addWidget(self.lbl_status, 5, 0, 1, 2)
        # create connetion
        self.btn_start.released.connect(self.start_wifi)
        btn_close.released.connect(self.close_wifi)
        chk_showpw.toggled[bool].connect(
                lambda flg : 
                self.txt_key.setEchoMode(qt.QLineEdit.Normal) if flg else self.txt_key.setEchoMode(qt.QLineEdit.Password))

    # slot function
    @qt.pyqtSlot()
    def start_wifi(self):
        msg = self.get_time() + self.tr("Starting Wifi......\n")
        ret = self.__ws.create_wifi(s = self.txt_ssid.text(), k = self.txt_key.text())
        if 0 == ret[0]:
            msg += self.get_time() + ret[1]
            ret = self.__ws.start_wifi()
            if 0 == ret[0]:
                msg += self.get_time() + ret[1]
                msg += self.get_time() + self.tr("Started Wifi")
                self.lbl_status.setText(msg)
                self.btn_start.released.disconnect(self.start_wifi)
                self.btn_start.released.connect(self.restart_wifi)
                self.btn_start.setText(self.tr("ReStart"))
                self.status = self.status_code[1]
                return True
        # failed to create or start wifi
        msg = self.get_time() + self.tr("Error: check Admin!")
        self.lbl_status.setText(msg)
        return False

    @qt.pyqtSlot()
    def restart_wifi(self):
        msg = self.get_time() + self.tr("Closing Wifi......\n")
        ret = self.__ws.close_wifi()
        if 0 == ret[0]:
            msg += self.get_time() + ret[1]
            msg += self.get_time() + self.tr("Restarting wifi......\n")
            ret = self.__ws.create_wifi(s = self.txt_ssid.text(), k = self.txt_key.text())
            if 0 == ret[0]:
                msg += self.get_time() + ret[1]
                ret = self.__ws.start_wifi()
                if 0 == ret[0]:
                    msg += self.get_time() + ret[1]
                    msg += self.get_time() + self.tr("Started Wifi")
                    self.lbl_status.setText(msg)
                    return True
        # failed to restart wifi
        msg = self.get_time() + self.tr("Error: check Admin!")
        self.lbl_status.setText(msg)
        return False

    @qt.pyqtSlot()
    def close_wifi(self):
        if self.status == self.status_code[1]:
            self.status = self.status_code[0]
            msg = self.get_time() + self.tr("Closing Wifi......\n")
            ret = self.__ws.close_wifi()
            if 0 == ret[0]:
                msg += self.get_time() + ret[1]
                msg += self.get_time() + self.tr("Closed wifi")
                self.lbl_status.setText(msg)
                self.btn_start.released.disconnect(self.restart_wifi)
                self.btn_start.released.connect(self.start_wifi)
                self.btn_start.setText(self.tr("Start"))
                return True
            # failed to close wifi
            msg = self.get_time() + self.tr("Error: check Admin!")
            self.lbl_status.setText(msg)
            return False

    # get current time
    def get_time(self):
        return "[" + qt.QTime.currentTime().toString() + "] "

    # event
    def keyReleaseEvent(self, event):
        if qt.Qt.Key_Escape == event.key():
            self.close()


#===============================================================================
# main-loop
#===============================================================================
if __name__ == "__main__":
    trans = qt.QTranslator()
    trans.load("lang/zh_CN")
    app = qt.QApplication(sys.argv)
    app.installTranslator(trans)
    mws = MiniWS()
    mws.show()
    app.exec()

