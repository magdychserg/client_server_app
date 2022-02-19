import argparse
import json
import logging
from socket import socket, SOL_SOCKET, SO_REUSEADDR
import sys
import socket
from common.utils import get_message, send_message
from common.variables import MAX_CONNECTIONS, ACTION, TIME, USER, ACCOUNT_NAME, PRESENCE, RESPONCE, \
    RESPONDEFAULT_IP_ADDRESS, ERROR, DEFAULT_PORT
from errors import IncorrectDataRecivedError
import logs.server_log_config

SERVER_LOGGER = logging.getLogger('server')

def process_client_message(message):
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message and message[USER][
        ACCOUNT_NAME] == 'Guest':
        return {RESPONCE: 200}
    return {
        RESPONDEFAULT_IP_ADDRESS: 400,
        ERROR: 'Bad request'
    }
def create_arg_parser():

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser

def main():
    try:
        parser = create_arg_parser()
        namespace = parser.parse_args(sys.argv[1:])
        listen_address = namespace.a
        listen_port = namespace.p
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        SERVER_LOGGER.critical(f'После -p необходимо указать номер порта.')
        print('После -p необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                                f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        print('номер порта в пределах от 1024 до 65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''
    except IndexError:
        SERVER_LOGGER.critical(f'После -а необходимо указать адрес.')
        print(' После -а необходимо указать адрес')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')
        try:
            message_from_client = get_message(client)
            SERVER_LOGGER.debug(f'Получено сообщение {message_from_client}')
            print(message_from_client)
            response = process_client_message(message_from_client)
            SERVER_LOGGER.info(f'Cформирован ответ клиенту {response}')
            send_message(client, response)
            SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрывается.')
            client.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать JSON строку, полученную от '
                                f'клиента {client_address}. Соединение закрывается.')
            client.close()
        except IncorrectDataRecivedError:
            SERVER_LOGGER.error(f'От клиента {client_address} приняты некорректные данные. '
                                f'Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()
