from DoAnCuoiKy.libs.JsonFactory import JsonFileFactory
from DoAnCuoiKy.models.Manager import Manager

managers=[]
managers.append(Manager("M1","Trương Thị Thuỳ Trinh","trinh","567"))
managers.append(Manager("M2","Trần Bảo Anh","anh","678"))
print("Danh sách Managers:")
for m in managers:
    print(m)
jff=JsonFileFactory()
filename="../dataset/managers.json"
jff.write_data(managers,filename)