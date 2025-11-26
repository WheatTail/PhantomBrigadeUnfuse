import oyaml as yaml
import zipfile
import os
import glob
import shutil
import winsound

#Путь к архиву
zip_path = 'unfuse/content.zip'
#Временная папка для распакованных данных
temp_dir = 'unpacked_archive'

def unfuse(data, new_value):
    if isinstance(data, dict):
        if "perk_1" in data and isinstance(data["perk_1"], dict):
            if "fused" in data["perk_1"]:
                data["perk_1"]["fused"] = new_value
                print(f"Отварено: {data['perk_1']['blueprint']}")
                
        for key, value in data.items():
            unfuse(value, new_value)
    elif isinstance(data, list):
        for item in data:
            unfuse(item, new_value)

#Обрабатываем по одному значению
def unfuse_perks_from_units(unit):
    with open(unit, 'r', encoding='utf-8') as unit_file:
        units = yaml.safe_load(unit_file)
        
    unfuse(units, "false")
        
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
#Получаем файл инвентаря базы
base_file = glob.glob('unpacked_archive/OverworldEntities/internal_mobilebase.yaml')
    
#Отвариваем на юнитах
for unit in unit_files:
    unfuse_perks_from_units(unit)
    
for unit in unit_files:
    with open(unit, 'r') as file:
        content = file.read().replace('null', '')
    with open(unit, 'w') as file:
        file.write(content)

#Отвариваем на базе
with open(base_file[0], 'r', encoding='utf-8') as file:
    base = yaml.safe_load(file)

unfuse(base, "false")
    
with open(base_file[0], 'w') as file:
    yaml.safe_dump(base, file)

with open(base_file[0], 'r') as file:
    content = file.read().replace('null', '')
with open(base_file[0], 'w') as file:
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

#Пищалка    
frequency = 1500
duration = 500
winsound.Beep(frequency, duration)