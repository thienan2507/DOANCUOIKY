from DoAnCuoiKy.libs.JsonFactory import JsonFileFactory
from DoAnCuoiKy.models.Material import Material

materials=[]
materials.append(Material('Gạo','Dài hạn',"Bà Năm",20000,50,25000,30,60 ))
print("Danh sách nguyên liệu:")
for m in materials:
    print(m)
jff=JsonFileFactory()
filename='../dataset/materials.json'
jff.write_data(materials,filename)