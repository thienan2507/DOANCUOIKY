from DoAnCuoiKy.libs.JsonFactory import JsonFileFactory
from DoAnCuoiKy.models.Employee import Employee

employees=[]
employees.append(Employee("E1","Nguyễn Thị Thiên Ân","an","123"))
employees.append(Employee("E2","Nguyễn Thị Mỹ Duyên","duyen","234"))
employees.append(Employee("E3","Nguyễn Thị Thu Hồng","hong","456"))

print("Danh sách Employee:")
for e in employees:
    print(e)
jff=JsonFileFactory()
filename="../dataset/employees.json"
jff.write_data(employees,filename)


