from PyQt6.QtWidgets import QMessageBox, QMainWindow

from DoAnCuoiKy.libs.DataConnector import DataConnector
from DoAnCuoiKy.ui.LoginMainWindow import Ui_MainWindow
from DoAnCuoiKy.ui.ManagerMainWindowExt import ManagerMainWindowExt
from DoAnCuoiKy.ui.MaterialManagementExt import MaterialManagementExt


class LoginMainWindowExt(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButtonLogin.clicked.connect(self.process_login)
        self.pushButtonExit.clicked.connect(self.process_exit)

    def process_login(self):
        #Kiểm tra thông tin đăng nhập và mở cửa sổ theo vai trò
        username = self.lineEditUserName.text().strip()
        password = self.lineEditPassword.text().strip()

        if not username or not password:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng nhập đầy đủ username và password!")
            return

        # Kiểm tra vai trò được chọn
        if self.radioButtonEmployee.isChecked():
            role = "Employee"
        elif self.radioButtonManager.isChecked():
            role = "Manager"
        else:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng chọn vai trò!")
            return

        # Kiểm tra đăng nhập với database
        dc = DataConnector()
        user = dc.login(username, password, role)

        if user:  # Đăng nhập thành công
            self.MainWindow.close()
            self.mainwindow = QMainWindow()
        #nếu là quản lỉ => mở cửa sổ quản lí
        #nếu là nhân vien => mở cửa sổ quản lí nguyên liệu
            if role == "Manager":
                self.myui = ManagerMainWindowExt(role)
            else:
                self.myui = MaterialManagementExt(role)

            self.myui.setupUi(self.mainwindow)
            self.myui.showWindow()
        else:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")

    def process_exit(self):
        #Xác nhận thoát chương trình
        msgbox = QMessageBox(self.MainWindow)
        msgbox.setText("Chắc chắn thoát?")
        msgbox.setWindowTitle("Xác nhận thoát")
        msgbox.setIcon(QMessageBox.Icon.Critical)
        buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        msgbox.setStandardButtons(buttons)
        if msgbox.exec() == QMessageBox.StandardButton.Yes:
            exit()
