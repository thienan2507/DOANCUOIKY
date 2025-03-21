from DoAnCuoiKy.libs.JsonFactory import JsonFileFactory
from DoAnCuoiKy.models.Material import Material

jff=JsonFileFactory()
filename='../dataset/materials.json'
maierials=jff.read_data(filename,Material)
for mt in maierials:
    print(mt)
