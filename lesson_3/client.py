### Функции клиента:
# - сформировать presence-сообщение;
# - отправить сообщение серверу;
# - получить ответ сервера;
# - разобрать сообщение сервера;
# - параметры командной строки скрипта client.py <addr> [<port>]: addr — ip-адрес сервера;
# - port — tcp-порт на сервере, по умолчанию 7777.

from sys import argv
from socket import *
from common.variables import *
from common.utils import *


def msg_prepare(account_name='Guest'):
    msg = {
        'action': 'presence',
        'time': time.time(),
        'user': {
            'account_name': account_name
        }
    }
    return msg

def start_connection(addr='127.0.0.1', port=DEFAULT_PORT):
    print(addr, port)
    s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
    s.connect((addr, port))  # Соединиться с сервером
    msg_to_sent = msg_prepare()
    # print(msg_to_sent)
    send_message(s, msg_to_sent)

    msg = get_message(s)

    print("Сообщение от сервера: %s" % msg)
    s.close()


def main():
    if len(argv) == 3:
        addr = argv[1]
        port = int(argv[2])
        if port < 1024 or port > 65535:
            print('Указан неверный порт')
        else:
            start_connection(addr, port)

    elif len(argv) == 2:
        addr = argv[1]
        start_connection(addr)
    else:
        start_connection()


if __name__ == '__main__':
    main()