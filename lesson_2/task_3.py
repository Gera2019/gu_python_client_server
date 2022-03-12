# 3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение
# данных в файле YAML-формата. Для этого:
#
# Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число,
# третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в
# кодировке ASCII (например, €);
# Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию
# файла с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
# Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
import os

import yaml
from yaml import Loader

PATH = 'data'
data = {'x':[], 'y':45, 'z':{'a':'45€', 'b':'40€', 'c':'50€'}}

def write_to_yaml():
        with open(os.path.join(PATH, 'file.yaml'), encoding='utf-8', mode='w') as f:
            yaml.dump(data, f, default_flow_style=True, allow_unicode=True)

def read_from_yaml():
    with open(os.path.join(PATH, 'file.yaml'), encoding='utf-8', mode='r') as f:
        obj = yaml.load(f, Loader=Loader)

    return obj

write_to_yaml()

# Проверка
print(read_from_yaml() == data)
