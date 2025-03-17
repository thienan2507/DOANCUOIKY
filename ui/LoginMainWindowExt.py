from PyQt6.QtWidgets import QMessageBox, QMainWindow

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
    #hàm kiểm tra thông tin nhập người dùng và xác định vai trò user
        username = self.lineEditUserName.text()
        password = self.lineEditPassword.text()
        if not username or not password:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng nhập đầy đủ username và password!")
            return
            # Xác định vai trò từ radio button
        if self.radioButtonEmployee.isChecked():
            role = "Employee"
        elif self.radioButtonManager.isChecked():
            role = "Manager"
        else:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng chọn vai trò!")
            return
        # Kết nối database
        dc = DataConnector()
        user = dc.login(username, password, role)  # Truy vấn user theo role => thuc hiện login
        #nếu thành công
        if user:
            self.MainWindow.close()
            self.mainwindow = QMainWindow()
            self.myui = MaterialManagementExt(role) #mo cửa sổ nguyên liệu theo vai trò
            self.myui.setupUi(self.mainwindow)
            self.myui.showWindow()
        else:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")

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




