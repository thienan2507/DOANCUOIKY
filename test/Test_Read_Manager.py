from DoAnCuoiKy.libs.JsonFactory import JsonFileFactory
from DoAnCuoiKy.models.Manager import Manager

jff=JsonFileFactory()
filename="../dataset/managers.json"
managers=jff.read_data(filename,Manager)
print("Danh sách Managers sau khi đọc file:")
for m in managers:
    print(m)
