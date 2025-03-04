import functools
import os
import webbrowser

from PyQt6.QtWidgets import QPushButton, QMessageBox, QMainWindow

from DoAnCuoiKy.libs.DataConnector import DataConnector
from DoAnCuoiKy.libs.Tool import Tool
from DoAnCuoiKy.models.Material import Material
from DoAnCuoiKy.ui.DailySummaryExt import DailySummaryExt
from DoAnCuoiKy.ui.MaterialManagement import Ui_mainWindow


class MaterialManagementExt(Ui_mainWindow):
    def __init__(self):
        self.dc=DataConnector()
        self.materials=[]
        self.employees=[]
        self.materials=self.dc.get_all_materials()
        self.employees=self.dc.get_all_employees()
        self.selected_material = None
        self.daily_summary_window = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.hienthi_sp_len_giaodien()
        self.setupSignalAndSlot()

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButtonSave.clicked.connect(self.xuly_luu)
        self.pushButtonUpdate.clicked.connect(self.xuly_capnhat)
        self.pushButtonRemove.clicked.connect(self.xuly_xoa)
        self.pushButtonClear.clicked.connect(self.xuly_clear)
        self.pushButtonSearch.clicked.connect(self.xuly_tim_kiem)
        self.pushButtonFilterType.clicked.connect(self.xuly_loc_loai)
        self.actionExport_To_Excel_File.triggered.connect(self.export_to_excel)
        self.actionImport_from_Excel.triggered.connect(self.import_from_excel)
        self.actionExit.triggered.connect(self.exit_program)
        self.actionHelp.triggered.connect(self.open_help)
        self.actionAbout.triggered.connect(self.open_about)
        self.pushButtonDailySummary.clicked.connect(self.show_daily_summary)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def hienthi_sp_len_giaodien(self, materials=None):
    #Hiển thị danh sách nguyên liệu lên giao diện. Nếu materials=None, hiển thị toàn bộ nguyên liệu.
        self.clearLayout(self.verticalLayoutButton)  # Xóa layout cũ trước khi cập nhật danh sách mới
        # Nếu không có danh sách tìm kiếm, hiển thị toàn bộ nguyên liệu
        if materials is None:
            materials = self.materials
        for mt in materials:
            btn = QPushButton(text=str(mt))
            self.verticalLayoutButton.addWidget(btn)
            btn.clicked.connect(functools.partial(self.xem_chi_tiet, mt))

    def xem_chi_tiet(self, mt):
    #xem chi tiết details
        self.lineEditName.setText(str(mt.name))
        self.lineEditSupplier.setText(str(mt.supplier))
        # Chuyển đổi số thành chuỗi, tránh lỗi khi `None`
        self.lineEditImportPrice.setText(str(mt.import_price))
        self.lineEditQuantityImported.setText(str(mt.import_qty))
        self.lineEditSellingPrice.setText(str(mt.sell_price))
        self.lineEditQuantitySold.setText(str(mt.sold_qty))
        self.lineEditExpectedUsageDays.setText(str(mt.use_day))
        if mt.type == "Ngắn hạn":
            self.radioButtonShortterm.setChecked(True)
        else:
            self.radioButtonLongterm.setChecked(True)
        self.selected_material = mt

    def xuly_luu(self):
    #nếu nguyên liệu có sẵn => cập nhật, nếu không có => lưu mới
        name = self.lineEditName.text().strip()
        supplier = self.lineEditSupplier.text().strip()
        import_price = int(self.lineEditImportPrice.text().strip())
        import_qty = float(self.lineEditQuantityImported.text().strip())
        sell_price = int(self.lineEditSellingPrice.text().strip())
        sold_qty = float(self.lineEditQuantitySold.text().strip())
        use_day = int(self.lineEditExpectedUsageDays.text().strip())
        type = 'Ngắn hạn' if self.radioButtonShortterm.isChecked() else 'Dài hạn'
        # Kiểm tra số âm
        if import_price < 0 or import_qty < 0 or sell_price < 0 or sold_qty < 0 or use_day < 0:
            raise ValueError("Giá và số lượng không thể âm.")
        # Tạo đối tượng nguyên liệu
        material = Material(name, type, supplier, import_price, import_qty, sell_price, sold_qty, use_day)
        # Tìm xem nguyên liệu đã tồn tại chưa
        index = self.dc.find_index_material(name)
        if index == -1:#chưa tồn tại
            self.dc.save_new_material(material)  #gọi hàm lưu mới
            QMessageBox.information(self.MainWindow, "Thành công", "Nguyên liệu đã được thêm mới!")
        else:#đã tồn tại
            self.dc.save_update_material(material)  # ✅ Gọi hàm cập nhật
            QMessageBox.information(self.MainWindow, "Thành công", "Nguyên liệu đã được cập nhật!")
        # Cập nhật lại danh sách hiển thị
        self.materials = self.dc.get_all_materials()
        self.hienthi_sp_len_giaodien()
        self.xuly_clear()#sau khi hoàn thành => clear details

    def xuly_xoa(self):
        name = self.lineEditName.text()
        #hiển thị cửa sổ cảnh báo
        msgbox = QMessageBox(self.MainWindow)
        msgbox.setWindowTitle("Xác nhận xóa")
        msgbox.setText(f"Xác nhận xóa [{name}] ?")
        msgbox.setIcon(QMessageBox.Icon.Critical)
        buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        msgbox.setStandardButtons(buttons)
        if msgbox.exec() == QMessageBox.StandardButton.No:#nếu bấm "No"=> quay về
            return
        # Xóa dữ liệu trong file JSON
        self.dc.delete_material(name)
        # Load lại danh sách nguyên liệu
        self.materials = self.dc.get_all_materials()
        # Cập nhật giao diện
        self.hienthi_sp_len_giaodien()
        self.xuly_clear()

    def xuly_clear(self):
        # hiển thị details trống
        self.lineEditName.clear()
        self.lineEditSupplier.clear()
        self.lineEditImportPrice.clear()
        self.lineEditQuantityImported.clear()
        self.lineEditSellingPrice.clear()
        self.lineEditQuantitySold.clear()
        self.lineEditExpectedUsageDays.clear()
        # Tắt chế độ chọn độc quyền để có thể bỏ chọn cả hai
        self.radioButtonLongterm.setAutoExclusive(False)
        self.radioButtonShortterm.setAutoExclusive(False)
        self.radioButtonLongterm.setChecked(False)
        self.radioButtonShortterm.setChecked(False)
        # Bật lại chế độ chọn độc quyền
        self.radioButtonLongterm.setAutoExclusive(True)
        self.radioButtonShortterm.setAutoExclusive(True)

    def xuly_capnhat(self):
    #cập nhật số lượng cho ngày sau
    #số lượng mới = số lượng nhập - số lượng bán
    #ngày sử dụng mới = ngày sử dụng cũ -1
        if not self.materials:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Không có nguyên liệu nào để cập nhật!")
            return
            # Duyệt qua toàn bộ nguyên liệu để cập nhật số lượng và số ngày sử dụng
        for mt in self.materials:
            if mt.import_qty is not None and mt.sold_qty is not None and mt.use_day is not None:
                #Tính số lượng mới
                new_import_qty = max(0, mt.import_qty - mt.sold_qty)
                new_use_day = max(0, mt.use_day - 1)
                new_sold_qty=0
                #Cập nhật dữ liệu
                mt.import_qty = new_import_qty
                mt.use_day = new_use_day
                mt.sold_qty=new_sold_qty
                #Lưu vào DataConnector
                self.dc.save_update_material(mt)
        # Cập nhật giao diện hiển thị
        self.hienthi_sp_len_giaodien()
        QMessageBox.information(self.MainWindow, "Thành công", "Tất cả nguyên liệu đã được cập nhật cho ngày mai!")

    def xuly_tim_kiem(self):
        #Tìm kiếm nguyên liệu theo tên và cập nhật danh sách hiển thị
        material_name = self.lineEditSearch.text().strip()  # Lấy tên nhập vào
        if not material_name:
            QMessageBox.warning(self.MainWindow, "Warning", "Vui lòng nhập tên nguyên liệu để tìm kiếm!")
            return
        # Lọc danh sách nguyên liệu
        filtered_materials = [mt for mt in self.materials if material_name.lower() in mt.name.lower()]
        if filtered_materials:
            self.hienthi_sp_len_giaodien(filtered_materials)  # Hiển thị danh sách tìm kiếm
        else:
            QMessageBox.warning(self.MainWindow, "Error", "Không tìm thấy nguyên liệu!")

    def xuly_loc_loai(self):
    #lọc nguyên liệu theo type: ngắn/dài hạn
        selected_type = self.comboBox.currentText()
        # Chuyển đổi giá trị để khớp với dữ liệu có sẵn
        if selected_type == "Short-term":
            selected_type = "Ngắn hạn"
        elif selected_type == "Long-term":
            selected_type = "Dài hạn"
        elif selected_type == "All":  # Nếu chọn "All", hiển thị tất cả nguyên liệu
            self.hienthi_sp_len_giaodien(self.materials)
            return  # Thoát luôn không cần lọc nữa
        # Lọc danh sách theo loại đã chọn
        filtered_materials = [mt for mt in self.materials if mt.type == selected_type]
        self.hienthi_sp_len_giaodien(filtered_materials)

    def xuly_tong(self):
        # Tổng chi phí nguyên liệu nhập vào 1 ngày = (số lượng nhập * giá nhập)/số ngày
        total_material_cost = 0
        for mt in self.materials:
            if mt.import_price and mt.import_qty and mt.use_day and int(mt.use_day) > 0:  # Kiểm tra tránh chia 0
                total_material_cost += (int(mt.import_price) * int(mt.import_qty)) / int(mt.use_day)
        # Tổng doanh thu 1 ngày = số lượng bán * giá bán
        total_revenue = sum(int(mt.sell_price) * int(mt.sold_qty) for mt in self.materials if mt.sell_price and mt.sold_qty)
        # Lợi nhuận 1 ngày = doanh thu - chi phí
        profit = total_revenue - total_material_cost
        #làm tròn
        return round(total_material_cost), round(total_revenue), round(profit)

    def show_daily_summary(self):
    #hiện cửa sổ thông báo chi phí, doanh thu, lợi nhuận
        if not self.daily_summary_window:
            self.daily_summary_window = QMainWindow()
            self.ui_daily_summary = DailySummaryExt()  # Dùng class mở rộng
            self.ui_daily_summary.setupUi(self.daily_summary_window)
        # Tính toán tổng hợp dữ liệu
        total_material_cost, total_revenue, profit = self.xuly_tong()
        # Hiển thị dữ liệu lên giao diện
        self.ui_daily_summary.lineEdit_MaterialCost.setText(str(total_material_cost))
        self.ui_daily_summary.lineEdit_Revenue.setText(str(total_revenue))
        self.ui_daily_summary.lineEdit_Profit.setText(str(profit))
        # Hiển thị cửa sổ
        self.ui_daily_summary.showWindow()

    def export_to_excel(self):
        filename = '../dataset/materials.xlsx'
        extool = Tool()
        extool.export_materials_to_excel(filename,self.materials)
        msgbox = QMessageBox(self.MainWindow)
        msgbox.setText("Đã export thành công")
        msgbox.setWindowTitle("Thông báo")
        msgbox.exec()

    def import_from_excel(self):
        filename = "../dataset/materials.xlsx"
        imtool = Tool()
        self.materials = imtool.import_material_from_excel(filename)
        self.hienthi_sp_len_giaodien()
        msgbox = QMessageBox(self.MainWindow)
        msgbox.setText("Đã import thành công")
        msgbox.setWindowTitle("Thông báo")
        msgbox.exec()

    def exit_program(self):
        msgbox = QMessageBox(self.MainWindow)
        msgbox.setText("Bạn có chắc muốn thoát phần mềm không?")
        msgbox.setWindowTitle("Xác nhận thoát")
        msgbox.setIcon(QMessageBox.Icon.Question)
        msgbox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if msgbox.exec() == QMessageBox.StandardButton.Yes:
            exit()

    def open_about(self):
        file_about = "ABOUT.pdf"
        current_path = os.getcwd()
        file_about = f"{current_path}/../assets/{file_about}"
        webbrowser.open_new(file_about)

    def open_help(self):
        file_help = "HELP.pdf"
        current_path = os.getcwd()
        file_help = f"{current_path}/../assets/{file_help}"
        webbrowser.open_new(file_help)









