from PyQt6.QtWidgets import QMainWindow, QMessageBox

from DoAnCuoiKy.libs.DataConnector import DataConnector
from DoAnCuoiKy.ui.LoginMainWindow import Ui_MainWindow
from DoAnCuoiKy.ui.MaterialManagementExt import MaterialManagementExt


class LoginMainWindowExt(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButtonLogin.clicked.connect(self.process_login)
        self.pushButtonExit.clicked.connect(self.process_exit)

    def process_login(self):
    #button login
        dc = DataConnector()
        uid = self.lineEditUserName.text()
        pwd = self.lineEditPassword.text()
        emp = dc.login(uid, pwd)
        if emp != None:
            self.MainWindow.close()  # close login window
            self.mainwindow = QMainWindow()
            self.myui = MaterialManagementExt()
            self.myui.setupUi(self.mainwindow)
            self.myui.showWindow()
        else:
            self.msg = QMessageBox(self.MainWindow)
            self.msg.setText("Đăng nhập thất bại")
            self.msg.exec()

    def process_exit(self):
    #button exit
        msgbox = QMessageBox(self.MainWindow)
        msgbox.setText("Chắc chắn thoát?")
        msgbox.setWindowTitle("Xác nhận thoát")
        msgbox.setIcon(QMessageBox.Icon.Critical)
        buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        msgbox.setStandardButtons(buttons)
        if msgbox.exec() == QMessageBox.StandardButton.Yes:
            exit()




