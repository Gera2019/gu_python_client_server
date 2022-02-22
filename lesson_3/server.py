### Функции сервера:
# - принимает сообщение клиента;
# - формирует ответ клиенту;
# - отправляет ответ клиенту;
# - имеет параметры командной строки: -p <port> — TCP-порт для работы (по умолчанию использует 7777);
# - -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
from sys import argv
from socket import socket, AF_INET, SOCK_STREAM
from common.variables import DEFAULT_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message
import unittest

def response_prepare(msg):
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
        response = response_prepare(msg_received)
        send_message(client, response)
        client.close()

def get_parameters():
    print(argv[1:])
    args = argv[1:]
    address, port = DEFAULT_ADDRESS, DEFAULT_PORT
    if args:
        try:
            if len(args) == 4:
                address = args[args.index('-a') + 1]
                port = int(args[args.index('-p') + 1])
                if port < 1024 and port > 65535:
                    raise ValueError
                else:
                    return address,port
            elif len(args) == 2:
                address = args[args.index('-a') + 1]
                return address, port
            else: raise ValueError

        except IndexError:
            print(IndexError, 'Введены некорректные параметры')

        except ValueError:
            print(ValueError, 'Введены некорректные параметры')
    else:
        return address,port






def main():
    parameters = get_parameters()
    try:
        server_start(*parameters)
    except OSError:
        print('Введены некорректные параметры')


if __name__ == '__main__':
    main()