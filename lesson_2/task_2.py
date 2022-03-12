# 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
# Написать скрипт, автоматизирующий его заполнение данными.

# Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
# цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл
# orders.json. При записи данных указать величину отступа в 4 пробельных символа;
# Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
import json
import os

PATH = 'data'
def write_order_to_json(item, quantity, price, buyer, date):
    order = {'item':item, 'quantity':quantity, 'price':price,'buyer':buyer, 'date':date}

    with open(os.path.join(PATH, 'orders.json'), encoding='utf-8') as f:
        orders = json.load(f)

    orders['orders'].append(order)

    with open(os.path.join(PATH, 'orders.json'), encoding='utf-8', mode='w') as f:
        json.dump(orders, f, indent=4)

write_order_to_json('Moon', '10', '10.5', 'Gary Gary', '22.04.2021')
write_order_to_json('Cat', '5', '16', 'Oleg Jay', '25.04.2021')