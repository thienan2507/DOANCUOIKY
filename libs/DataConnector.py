from DoAnCuoiKy.libs.JsonFactory import JsonFileFactory
from DoAnCuoiKy.models.Employee import Employee
from DoAnCuoiKy.models.Material import Material


class DataConnector:
    def get_all_materials(self):
    #lấy tất cả thông tin nguyên liệu
        jff=JsonFileFactory()
        filename='../dataset/materials.json'
        materials=jff.read_data(filename,Material)
        return materials

    def get_all_employees(self):
    #lấy tất cả thông tin nhân viên
        jff = JsonFileFactory()
        filename = '../dataset/employees.json'
        employees = jff.read_data(filename, Employee)
        return employees

    def login(self,username,password):
    #đăng nhập ở màn hình login
    #lấy thông tin nhân viên
    #kiểm tra tên đăng nhập có trùng khớp với tên đăng nhập trong dữ liệu sẵn có không
        employees=self.get_all_employees()
        for e in employees:
            if e.UserName==username and e.Password == password:
                return e
        return None

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

    def delete_material(self,name):
    #chức năng xóa
        index=self.find_index_material(name)
        if index !=-1:
            self.materials.pop(index)
            jff = JsonFileFactory()
            filename = "../dataset/materials.json"
            jff.write_data(self.materials, filename)

    def save_new_material(self,material):
    #chức năng thêm mới
        materials = self.get_all_materials()
        materials.append(material)
        jff = JsonFileFactory()
        filename = "../dataset/materials.json"
        jff.write_data(materials, filename)

    def save_update_material(self,current_material):
    #chức năng cập nhật
        index=self.find_index_material(current_material.name)
        if index !=-1:
            self.materials[index]=current_material
            jff = JsonFileFactory()
            filename = "../dataset/materials.json"
            jff.write_data(self.materials, filename)