from DoAnCuoiKy.libs.JsonFactory import JsonFileFactory
from DoAnCuoiKy.models.Employee import Employee

employees=[]
employees.append(Employee("E1","Nguyễn Thị Thiên Ân","an","123"))
employees.append(Employee("E2","Nguyễn Thị Mỹ Duyên","duyen","234"))
employees.append(Employee("E3","Nguyễn Thị Thu Hồng","hong","456"))
employees.append(Employee("E4","Trương Thị Thuỳ Trinh","trinh","567"))
employees.append(Employee("E5","Trần Bảo Anh","anh","678"))
print("Danh sách Employee:")
for e in employees:
    print(e)
jff=JsonFileFactory()
filename="../dataset/employees.json"
jff.write_data(employees,filename)