import functools
import os
import webbrowser

from PyQt6.QtWidgets import QPushButton, QMessageBox

from DoAnCuoiKy.libs.DataConnector import DataConnector
from DoAnCuoiKy.libs.Tool import Tool
from DoAnCuoiKy.models.Employee import Employee
from DoAnCuoiKy.ui.EmployeeManagement import Ui_mainWindow

class EmployeeManagementExt(Ui_mainWindow):
    def __init__(self):
        self.dc = DataConnector()
        self.employees = self.dc.get_all_employees()
        self.selected_employee = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.hienthi_nhanvien_len_giaodien()# Lưu cửa sổ chính
        self.setupSignalandSlot()

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalandSlot(self):
        self.pushButtonSave.clicked.connect(self.xuly_luu)
        self.pushButtonRemove.clicked.connect(self.xuly_xoa)
        self.pushButtonSearch.clicked.connect(self.xuly_timkiem)
        self.actionExport_To_Excel_File.triggered.connect(self.export_to_excel)
        self.actionImport_from_Excel.triggered.connect(self.import_from_excel)
        self.actionHelp.triggered.connect(self.open_help)
        self.actionAbout.triggered.connect(self.open_about)
        self.actionExit.triggered.connect(self.exit_program)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def hienthi_nhanvien_len_giaodien(self, employees=None):
        self.clearLayout(self.verticalLayoutButton)
        if employees is None:
            employees = self.employees
        for emp in employees:
            btn = QPushButton(text=str(emp))
            self.verticalLayoutButton.addWidget(btn)
            btn.clicked.connect(functools.partial(self.xem_chi_tiet, emp))

    def xem_chi_tiet(self, emp):
    #hàm xem chi tiết thông tin nhân viên
        self.lineEditEmpId.setText(str(emp.EmployeeId))
        self.lineEditEmpName.setText(emp.EmployeeName)
        self.lineEditEmUser.setText(emp.UserName)
        self.lineEditEmpPassword.setText(emp.Password)
        self.selected_employee=emp

    def xuly_clear(self):
        self.lineEditEmpName.clear()
        self.lineEditEmpId.clear()
        self.lineEditEmUser.clear()
        self.lineEditEmpPassword.clear()

    def xuly_luu(self):
    #hàm xử lý lưu
    #nếu nhân viên đã tồn tại => xử lí cập nhật thông tin nhân viên, không tồn tại => thêm moi
        emp_id = self.lineEditEmpId.text().strip()
        name = self.lineEditEmpName.text().strip()
        username = self.lineEditEmUser.text().strip()
        password = self.lineEditEmpPassword.text().strip()

        if not emp_id or not name or not username or not password:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            #đảm bảo người dùng nhập đầy đủ thông tin
            return

        employee = Employee(emp_id, name, username, password)
        index = self.dc.find_index_employee(emp_id)  # Tìm theo ID nhân viên

        if index == -1:#nếu nhân viên chưa tồn tại
            self.dc.save_new_employee(employee)
            QMessageBox.information(self.MainWindow, "Thành công", "Thêm nhân viên thành công!")
        else:
            self.dc.save_update_employee(employee)
            QMessageBox.information(self.MainWindow, "Thành công", "Cập nhật nhân viên thành công!")

        self.employees = self.dc.get_all_employees()
        self.hienthi_nhanvien_len_giaodien()
        self.xuly_clear()

    def xuly_xoa(self):
        emp_id = self.lineEditEmpId.text().strip()
        if not emp_id:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng chọn nhân viên!")
            return
        self.dc.delete_employee(emp_id)
        self.employees = self.dc.get_all_employees()  # Load lại danh sách
        self.hienthi_nhanvien_len_giaodien()  # Cập nhật giao diện
        self.xuly_clear()

    def xuly_timkiem(self):
        # Tìm kiếm nhân viên theo tên và cập nhật danh sách hiển thị
        employee_name = self.lineEditSearch.text().strip()  # Lấy tên nhập vào
        if not employee_name:
            QMessageBox.warning(self.MainWindow, "Warning", "Vui lòng nhập tên nhân viên để tìm kiếm!")
            return
        # Lọc danh sách nhân viên
        filtered_employees = [emp for emp in self.employees if employee_name.lower() in emp.EmployeeName.lower()]
        if filtered_employees:
            self.hienthi_nhanvien_len_giaodien(filtered_employees)  # Hiển thị danh sách tìm kiếm
        else:
            QMessageBox.warning(self.MainWindow, "Error", "Không tìm thấy nhân viên!")

    def export_to_excel(self):
        filename = '../dataset/employees.xlsx'
        extool = Tool()
        extool.export_employees_to_excel(filename, self.employees)
        msgbox = QMessageBox(self.MainWindow)
        msgbox.setText("Đã export thành công")
        msgbox.setWindowTitle("Thông báo")
        msgbox.exec()

    def import_from_excel(self):
        filename = "../dataset/employees.xlsx"
        imtool = Tool()
        self.materials = imtool.import_employee_from_excel(filename)
        self.hienthi_nhanvien_len_giaodien()
        msgbox = QMessageBox(self.MainWindow)
        msgbox.setText("Đã import thành công")
        msgbox.setWindowTitle("Thông báo")
        msgbox.exec()

    def open_help(self):
        file_help = "HELP.pdf"
        current_path = os.getcwd()
        file_help = f"{current_path}/../assets/{file_help}"
        webbrowser.open_new(file_help)

    def open_about(self):
        file_about = "ABOUT.pdf"
        current_path = os.getcwd()
        file_about = f"{current_path}/../assets/{file_about}"
        webbrowser.open_new(file_about)

    def exit_program(self):
        msgbox = QMessageBox(self.MainWindow)
        msgbox.setText("Bạn có chắc muốn thoát phần mềm không?")
        msgbox.setWindowTitle("Xác nhận thoát")
        msgbox.setIcon(QMessageBox.Icon.Question)
        msgbox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if msgbox.exec() == QMessageBox.StandardButton.Yes:
            exit()

