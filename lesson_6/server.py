### Функции сервера:
# - принимает сообщение клиента;
# - формирует ответ клиенту;
# - отправляет ответ клиенту;
# - имеет параметры командной строки: -p <port> — TCP-порт для работы (по умолчанию использует 7777);
# - -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).

from sys import argv, path
from socket import socket, AF_INET, SOCK_STREAM
from common.variables import DEFAULT_ADDRESS, DEFAULT_PORT, ACTION, ACCOUNT_NAME, PRESENCE, RESPONSE, USER, ERROR, TIME
from common.utils import get_message, send_message
import logging
import logs.server_log_cfg
from common.decorators import log

SERVER_LOGGER = logging.getLogger('server')

@log
def cmd_parse():
    args = argv[1:]
    address, port = DEFAULT_ADDRESS, DEFAULT_PORT
    if args:
        try:
            if len(args) == 4:
                address = args[args.index('-a') + 1]
                port = int(args[args.index('-p') + 1])
                if 1024 > port > 65535:
                    raise ValueError
                else:
                    return address,port
            elif len(args) == 2:
                address = args[args.index('-a') + 1]
                return address, port
            else:
                raise ValueError

        except IndexError:
            SERVER_LOGGER.critical(IndexError, 'Введены некорректные параметры')

        except ValueError:
            SERVER_LOGGER.critical(ValueError, 'Введены некорректные параметры')
    else:
        return address, port

@log
def process_client_msg(msg):
    if ACTION in msg and msg[ACTION] == PRESENCE and TIME in msg and USER in msg and msg[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Неправильный запрос'
    }

@log
def server_start(addr=DEFAULT_ADDRESS, port=DEFAULT_PORT):
    s = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
    s.bind((addr, port))
    s.listen(5)
    SERVER_LOGGER.info(f'Сервер запущен с параметрами: '
                       f'адрес сервера: {addr} , порт: {port}')

    while True:
        client, client_addr = s.accept()     # Принять запрос на соединение
        SERVER_LOGGER.info("Получен запрос на соединение от %s" % str(client_addr))
        msg_received = get_message(client)
        SERVER_LOGGER.info('server_start', msg_received)
        response = process_client_msg(msg_received)
        send_message(client, response)
        client.close()


def main():
    try:
        server_start(*cmd_parse())
    except OSError:
        SERVER_LOGGER.critical('Введены некорректные параметры')


if __name__ == '__main__':
    main()