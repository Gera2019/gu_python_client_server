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
import select

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
                    return address, port
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
def process_client_msg(msg, msg_list, client):
    if ACTION in msg and msg[ACTION] == PRESENCE and TIME in msg and USER in msg:
        send_message(client, {RESPONSE: 200})
        return
    elif ACTION in msg and msg[ACTION] == MESSAGE and TIME in msg and MESSAGE_TEXT in msg:
        msg_list.append((msg[ACCOUNT_NAME], msg[MESSAGE_TEXT]))
        return
    else:
        send_message (client, {
            RESPONSE: 400,
            ERROR: 'Неправильный запрос'
        })
        return


@log
def server_start(addr=DEFAULT_ADDRESS, port=DEFAULT_PORT):
    client_list = []
    s = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
    s.bind((addr, port))
    s.listen(5)
    s.settimeout(0.2)
    SERVER_LOGGER.info(f'Сервер запущен с параметрами: '
                       f'адрес сервера: {addr} , порт: {port}')

    msg_list = []
    client_list = []

    while True:
        try:
            client, client_addr = s.accept()  # Принять запрос на соединение
            print('client', client)
        except OSError as e:
            pass
        else:
            SERVER_LOGGER.info("Получен запрос на соединение от %s" % str(client_addr))
            client_list.append(client)

        if client_list:
            try:
                input, output, errors = select.select(client_list, client_list, [], 0)
            except Exception as e:
                # Исключение произойдет, если какой-то клиент отключится
                pass  # Ничего не делать, если какой-то клиент отключился

            if r:
                for s_client in input:
                    msg_received = get_message(s_client)
                    SERVER_LOGGER.info(f'Получено сообщение от {s_client}', msg_received)
                    try:
                        process_client_msg(msg_received, msg_list, s_client)
                        SERVER_LOGGER.info(f'Клиент {msg_received[USER][ACCOUNT_NAME]} подключился')
                    except:
                        # Удаляем клиента, который отключился
                        SERVER_LOGGER.info(f'Клиент {msg_received[USER][ACCOUNT_NAME]} отключился')
                        client_list.remove(s_client)

            if msg_list and output:
                message = {
                    ACTION: MESSAGE,
                    SENDER: msg_list[0][0],
                    TIME: time.time(),
                    MESSAGE_TEXT: msg_list[0][1]
                }
                del msg_list[0]
                for client in output:
                    try:
                        send_message(client, message)
                    except:
                        SERVER_LOGGER.info(f'Клиент {client.getpeername()} отключился от сервера.')
                        client.close()
                        client_list.remove(client)

def main():
    try:
        server_start(*cmd_parse())
    except OSError as msg:
        SERVER_LOGGER.critical(f'Ошибка запуска сервера - {msg}')


if __name__ == '__main__':
    main()
