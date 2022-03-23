from sys import argv,exit
from socket import socket, AF_INET, SOCK_STREAM
from common.variables import DEFAULT_ADDRESS, DEFAULT_PORT, ACTION, ACCOUNT_NAME, PRESENCE, RESPONSE, USER, ERROR, TIME, MESSAGE, MESSAGE_TEXT, DEFAULT_MODE, SENDER
from common.utils import send_message, get_message
from errors import ReqFieldMissingError
import time
import json
import logging
import logs.client_log_cfg
from common.decorators import log
# - port — tcp-порт на сервере, по умолчанию 7777.
import argparse

CLIENT_LOGGER = logging.getLogger('client')

@log
def cmd_parse(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(argv[1:])
    address = namespace.addr
    port = namespace.port
    mode = namespace.mode

    if port < 1024 or port > 65535:
        CLIENT_LOGGER.critical(
            f'Указан неверный порт: {port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        exit(1)
    if mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Указан неверный режим работы {mode}, допустимые режимы: listen , send')
        exit(1)
    return address, port, mode

@log
def create_presense(account_name='Guest'):
    msg = {
        ACTION: 'presence',
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return msg

@log
def message_from_server(message):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')


@log
def process_server_msg(message):

    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)

@log
def create_message(sock, account_name='Guest'):
    message = input('Введите сообщение или "Q" для завершения работы: ')
    if message == 'Q':
        sock.close()
        CLIENT_LOGGER.info('Работа завершена')
        exit(0)
    msg = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформировано сообщение {msg} для пользователя {account_name}')
    return msg


@log
def start_connection(addr=DEFAULT_ADDRESS, port=DEFAULT_PORT, mode=DEFAULT_MODE):
    s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
    s.connect((addr, port))  # Соединиться с сервером
    CLIENT_LOGGER.info(f'Клиент запущен с параметрами: '
                       f'адрес сервера: {addr} , порт: {port}')
    client_name = input('Введите имя пользователя: ')

    msg_to_sent = create_presense(client_name)
    send_message(s, msg_to_sent)
    CLIENT_LOGGER.info(f'Сообщение пользователя {client_name} отправлено')
    msg = get_message(s)
    response = process_server_msg(msg)
    CLIENT_LOGGER.info("Сообщение от сервера: %s" % response)
    connection_parameters = s, mode
    return connection_parameters

def process_chat(current_connection):
    conn_socket, mode = current_connection
    if mode == 'send':
        print('Режим работы - отправка сообщений.')
    else:
        print('Режим работы - приём сообщений.')
    while True:
        # режим работы - отправка сообщений
        if mode == 'send':
            try:
                send_message(conn_socket, create_message(conn_socket))
            except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                CLIENT_LOGGER.error(f'Соединение с сервером было потеряно.')
                exit(1)

        # Режим работы приём:
        if mode == 'listen':
            try:
                message_from_server(get_message(conn_socket))
            except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                CLIENT_LOGGER.error(f'Соединение с сервером было потеряно.')
                exit(1)


def main():
    address, port, mode = cmd_parse(argv)
    try:
        current_connection = start_connection(address, port, mode)

    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу')

    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')

    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')

    else:
        if current_connection:
            process_chat(current_connection)


if __name__ == '__main__':
    main()
