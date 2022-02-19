import argparse
import json
import logging
import socket
import sys
import time
import logs.client_log_config
from common.utils import send_message, get_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONCE, ERROR, DEFAULT_IP_ADDRESS, \
    DEFAULT_PORT
from errors import ReqFieldMissingError

CLIENT_LOGGER = logging.getLogger('client')

def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


def process_ans(message):
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONCE in message:
        if message[RESPONCE] == 200:
            return '200: OK'
        return f'400: {message[ERROR]}'
    raise ValueError

def create_arg_parser():

    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    return parser


def main():

    try:
        parser = create_arg_parser()
        namespace = parser.parse_args(sys.argv[1:])
        server_address = namespace.addr
        server_port = namespace.port
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
        CLIENT_LOGGER.info(f'Запущен клиент с парамертами: '
                           f'адрес сервера: {server_address}, порт: {server_port}')
    except ValueError:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        # print('Порт должен быть в диапазоне 1024 - 65535')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_presence()
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
        print(answer)
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    main()
