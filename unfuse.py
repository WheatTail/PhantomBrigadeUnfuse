import oyaml as yaml
import zipfile
import os
import glob
import shutil

#Кастомный конструктор, чтобы избавиться от null в пустых значениях, но забил
#def custom_oyaml_constructor(loader, node):
#    value = loader.construct_scalar(node)
#    if value == "":
#        return ''
#    return value
    
#yaml.SafeLoader.add_constructor("tag:yaml.org,2002:null", custom_oyaml_constructor)

#Путь к архиву
zip_path = 'unfuse/content.zip'
#Временная папка для распакованных данных
temp_dir = 'unpacked_archive'

#Проверяем, есть ли нужный ключ, в нашем случае - perk_1
def get_nested_fuse_value(unit, keys, default=""):
    for key in keys:
        if isinstance(unit, dict) and key in unit:
            unit = unit[key]
        else:
            return default
    return unit

#Устанавливаем нужное значение во fused:
def set_nested_fuse_value(unit, keys, value):
    #:-1 - срез всех элементов, кроме последнего, т.к. последний меняем
    for key in keys[:-1]:
        #если ключа нет
        if key not in unit or not isinstance(unit[key], dict):
            #Пропускаем
            continue
        #итерируемся по ключам
        unit = unit[key]
    #меняем значение последнего
    unit[keys[-1]] = value

#Список ключей и новое значение для fused:
unfused_perks = [
    (['parts', 'core', 'systems', 'perk_1', 'fused'], False),
    (['parts', 'secondary', 'systems', 'perk_1', 'fused'], False),
    (['parts', 'optional_left', 'systems', 'perk_1', 'fused'], False),
    (['parts', 'optional_right', 'systems', 'perk_1', 'fused'], False),
    (['parts', 'equipment_right', 'systems', 'perk_1', 'fused'], False),
    (['parts', 'equipment_left', 'systems', 'perk_1', 'fused'], False)    
]
#(['parts', 'back', 'systems', 'perk_1', 'fused'], False) для ранца, но у них нет перков

#Обрабатываем по одному значению
def unfuse_perks(unit):
    with open(unit, 'r', encoding='utf-8') as unit_file:
        units = yaml.safe_load(unit_file)
    
    for keys, value in unfused_perks:
        if get_nested_fuse_value(units, keys) is not None:
            set_nested_fuse_value(units, keys, value)
    
    with open(unit, 'w') as file:        
        yaml.safe_dump(units, file)

#Временная папка для распакованного архива
os.makedirs(temp_dir, exist_ok=True)

#Распаковка архива
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(temp_dir)

for root, _, files in os.walk(temp_dir):
    for file in files:
        file_path = os.path.join(root, file)
        print(f"Синхронизация файла: {file_path}")
        with open(file_path, 'r+') as f:
            os.fsync(f.fileno())

#Получаем массив файлов юнитов
unit_files = glob.glob('unpacked_archive/Units/*yaml')
    
for unit in unit_files:
    unfuse_perks(unit)
    
for unit in unit_files:
    with open(unit, 'r') as file:
        content = file.read().replace('null', '')
    with open(unit, 'w') as file:
        file.write(content)

#Пишем в архив        
with zipfile.ZipFile(zip_path, 'w') as zip_ref:
    #os.walk обходит папку рекурсивно
    for root, _, files in os.walk(temp_dir):
        for file in files:
            #os.path.join(root, file) - полный путь к файлу
            file_path = os.path.join(root, file)
            #Относительный путь к файлу, относительно temp_dir
            arcname = os.path.relpath(file_path, temp_dir)
            #Добавить в архив, сохраняя относительный путь
            zip_ref.write(file_path, arcname)
            
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)