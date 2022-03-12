### Функции клиента:
# - сформировать presence-сообщение;
# - отправить сообщение серверу;
# - получить ответ сервера;
# - разобрать сообщение сервера;
# - параметры командной строки скрипта client.py <addr> [<port>]: addr — ip-адрес сервера;
# - port — tcp-порт на сервере, по умолчанию 7777.

from sys import argv
from socket import socket, AF_INET, SOCK_STREAM
from common.variables import DEFAULT_ADDRESS, DEFAULT_PORT, ACTION, ACCOUNT_NAME, PRESENCE, RESPONSE, USER, ERROR, TIME
from common.utils import send_message, get_message
from errors import ReqFieldMissingError
import time
import json


def cmd_parse(arguments):
    if len(arguments) == 3:
        address = argv[1]
        port = int(argv[2])
        if port < 1024 or port > 65535:
            print('Указан неверный порт')
        else:
            return address, port

    elif len(arguments) == 2:
        address = argv[1]
        return address
    else:
        return ()


def process_client_msg(account_name='Guest'):
    msg = {
        ACTION: 'presence',
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return msg

def process_server_msg(message):
    """
    Функция разбирает ответ сервера
    :param message:
    :return:
    """

    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)

def start_connection(addr=DEFAULT_ADDRESS, port=DEFAULT_PORT):
    s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
    s.connect((addr, port))  # Соединиться с сервером

    msg_to_sent = process_client_msg()
    send_message(s, msg_to_sent)

    msg = get_message(s)
    response = process_server_msg(msg)
    print("Сообщение от сервера: %s" % response)
    s.close()

def main():
    try:
        start_connection(*cmd_parse(argv))

    except ConnectionRefusedError:
        print(f'Не удалось подключиться к серверу')

    except ReqFieldMissingError as missing_error:
        print(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')

    except json.JSONDecodeError:
        print('Не удалось декодировать полученную Json строку.')


if __name__ == '__main__':
    main()
