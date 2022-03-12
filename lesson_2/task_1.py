# 1. Задание на закрепление знаний по модулю CSV.
# Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и
# формирующий новый «отчетный» файл в формате CSV.

# Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание
# данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
# «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в
# соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
# os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и
# поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта»,
# «Тип системы». Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для
# каждого файла);
# Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение
# данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
# Проверить работу программы через вызов функции write_to_csv().
import os
import chardet
import re
import csv

PATH = 'data'

def get_data():

    main_data_headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data = [main_data_headers]
    data = []

# подготовим итоговый список
    for i in range(len(main_data_headers)):
        data.append([])

# определяем кодировкку
    for filename in os.listdir(PATH):
        with open(os.path.join(PATH, filename), 'rb') as fb:
            text = fb.read()
            encoding = chardet.detect(text)['encoding']

            # text_decoded = text.decode(encoding=encoding).split('\n')
            # не уверена, что делить строку по признаку новой строки правильно и универсально,
            # т.к. есть еще возврат каретки, и в новых системах этого символа может и не быть
        with open(os.path.join(PATH, filename), encoding=encoding ) as f:
            for line in f:
                for key, value in enumerate(main_data_headers):
                    data[key].extend(re.findall(rf'^{value}.\s*(.+)$', line))

    # формируем данные для отчета
    for i in zip(*data):
        main_data.append([*i])

    return main_data


def write_to_csv():
    with open(os.path.join(PATH, 'main_data.csv'), encoding='utf-8', mode='w') as f:
        f.writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        f.writer.writerows(get_data())


write_to_csv()