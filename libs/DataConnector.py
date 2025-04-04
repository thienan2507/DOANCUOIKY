from DoAnCuoiKy.libs.JsonFactory import JsonFileFactory
from DoAnCuoiKy.models.Employee import Employee
from DoAnCuoiKy.models.Manager import Manager
from DoAnCuoiKy.models.Material import Material


class DataConnector:
    def get_all_materials(self):
    #lấy tất cả thông tin nguyên liệu
        jff=JsonFileFactory()
        filename='../dataset/materials.json'
        materials=jff.read_data(filename,Material)
        return materials

    def get_all_employees(self):
    #lấy tất cả thông tin nhân vie
        jff = JsonFileFactory()
        filename = "../dataset/employees.json"
        employees = jff.read_data(filename, Employee)
        return employees

    def get_all_managers(self):
    #lấy tất cả thông tin của quản lí
        jff = JsonFileFactory()
        filename = '../dataset/managers.json'
        managers = jff.read_data(filename, Manager)
        return managers

    def get_all_users(self):
    #lấy thông tin của quản l và cả nhân viên để tạo hàm log in
        jff = JsonFileFactory()
        managers = jff.read_data("../dataset/managers.json", Manager)
        employees = jff.read_data("../dataset/employees.json", Employee)
        # Gán role
        for manager in managers:
            manager.Role = "Manager"
        for employee in employees:
            employee.Role = "Employee"
        users = managers + employees
        return users

    def login(self, username, password, role):
    #hàm xử lí username,password,role có trùng khớp không
        users = self.get_all_users()
        for user in users:
            if user.UserName == username and user.Password == password and user.Role == role:
                return user  # Nếu tìm thấy user hợp lệ, trả về ngay
        return None  # Trả về None để báo rằng đăng nhập thất bại

    def find_index_material(self,name):
    #tìm vị trí của nguyên liệu trong danh sách
    #duyệt qua từng nguyên liệu => so sánh tên có trùng khớp với nhau không
    #nếu có => trả về vị trí của nguyên liệu đó, nếu không khớp => trả về -1
        self.materials = self.get_all_materials()
        for i in range (len(self.materials)):
            material=self.materials[i]
            if material.name==name:
                return i
        return -1

    def find_index_employee(self, emp_id):
    #tim vị trí của nhân viên trong danh sách nhân viên
    #so sánh id có trùng khớp không
        employees = self.get_all_employees()
        for i in range(len(employees)):
            if employees[i].EmployeeId == emp_id:
                return i
        return -1

    def delete_material(self,name):
    #chức năng xóa nguyên liệu
        index=self.find_index_material(name)
        if index !=-1:
            self.materials.pop(index)
            jff = JsonFileFactory()
            filename = "../dataset/materials.json"
            jff.write_data(self.materials, filename)

    def delete_employee(self, emp_id):
    #chức năng xóa nhân viên
        employees = self.get_all_employees()
        index = self.find_index_employee(emp_id)
        if index != -1:
            employees.pop(index)  # Xóa nhân viên khỏi danh sách
            jff = JsonFileFactory()
            filename = "../dataset/employees.json"
            jff.write_data(employees, filename)  # Ghi lại danh sách mới

    def save_new_material(self,material):
    #chức năng thêm mới nguyên liệu
        materials = self.get_all_materials()
        materials.append(material)
        jff = JsonFileFactory()
        filename = "../dataset/materials.json"
        jff.write_data(materials, filename)

    def save_new_employee(self, employee):
    # chức năng thêm mới nhân viên
        employees = self.get_all_employees()
        employees.append(employee)
        jff = JsonFileFactory()
        filename = "../dataset/employees.json"
        jff.write_data(employees, filename)

    def save_update_material(self,current_material):
    #chức năng cập nhật nguyên liệu
        index=self.find_index_material(current_material.name)
        if index !=-1:
            self.materials[index]=current_material
            jff = JsonFileFactory()
            filename = "../dataset/materials.json"
            jff.write_data(self.materials, filename)

    def save_update_employee(self, current_employee):
    #chức năng cập nhật nhân viên
        employees = self.get_all_employees()  # Lấy danh sách mới nhất
        index = self.find_index_employee(current_employee.EmployeeId)  # Tìm theo ID
        if index != -1:
            employees[index] = current_employee
            jff = JsonFileFactory()
            filename = "../dataset/employees.json"
            jff.write_data(employees, filename)  # Lưu vào file
