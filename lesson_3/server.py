### Функции сервера:
# - принимает сообщение клиента;
# - формирует ответ клиенту;
# - отправляет ответ клиенту;
# - имеет параметры командной строки: -p <port> — TCP-порт для работы (по умолчанию использует 7777);
# - -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
from sys import argv
from socket import *
from common.variables import *
from common.utils import *

def responce_prepare(msg):
    print('response', msg)
    print(('action' in msg), (msg['action'] == 'presence'), ('user' in msg), (msg['user']['account_name'] == 'Guest'))
    if 'action' in msg and msg['action'] == 'presence' and 'user' in msg and msg['user']['account_name'] == 'Guest':
        return {'response': 200}
    return {
        'response': 400,
        'error_msg': 'Неправильный запрос'
    }

def server_start(addr=DEFAULT_ADDRESS, port=DEFAULT_PORT):
    s = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
    s.bind((addr, port))
    s.listen(5)
    print('Сервер запущен')

    while True:
        client, client_addr = s.accept()     # Принять запрос на соединение
        print("Получен запрос на соединение от %s" % str(client_addr))
        msg_received = get_message(client)
        print('server_start', msg_received)
        response = responce_prepare(msg_received)
        send_message(client, response)
        client.close()



def main():
    if len(argv) // 2 != 0:
        _ = {argv[i]: argv[i + 1] for i in range(1, len(argv), 2)}
        if _['-p']:
            int(_['-p'])
        args = (_['-a'], _['p'])

    elif len(argv) == 1:
        args = None

    else:
        print('Wrong parameters')

    if args:
        server_start(*args)
    else:
        server_start()

if __name__ == '__main__':
    main()