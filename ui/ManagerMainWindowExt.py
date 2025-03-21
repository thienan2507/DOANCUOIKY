from PyQt6.QtWidgets import QMainWindow

from DoAnCuoiKy.ui.EmployeeManagementExt import EmployeeManagementExt
from DoAnCuoiKy.ui.ManagerMainWindow import Ui_MainWindow
from DoAnCuoiKy.ui.MaterialManagementExt import MaterialManagementExt

class ManagerMainWindowExt(QMainWindow, Ui_MainWindow):
    def __init__(self, role):
        super().__init__()
        self.role = role
        # Lưu cửa sổ con để tránh bị đóng ngay
        self.material_management_window = None
        self.employee_management_window = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButtonMaterialManagement.clicked.connect(self.show_material_management)
        self.pushButtonEmployeeManagement.clicked.connect(self.show_employee_management)

    def show_material_management(self):
        if self.material_management_window is None:
            self.material_management_window = QMainWindow()  # Tạo cửa sổ cha
            self.ui_material_management = MaterialManagementExt(self.role)#mở cửa sổ quản lí nguyên liệu theo vai trò
            self.ui_material_management.setupUi(self.material_management_window)
        self.material_management_window.show()

    def show_employee_management(self):
        if self.employee_management_window is None:
            self.employee_management_window = QMainWindow()  # Tạo cửa sổ cha
            self.ui_employee_management = EmployeeManagementExt()  # Khởi tạo UI
            self.ui_employee_management.setupUi(self.employee_management_window)  # Gán UI vào cửa sổ
        self.employee_management_window.show()




