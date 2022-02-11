import json
import socket
import sys
import time

from common.utils import send_message, get_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONCE, ERROR, DEFAULT_IP_ADDRESS, \
    DEFAULT_PORT


def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def process_ans(message):
    if RESPONCE in message:
        if message[RESPONCE] == 200:
            return '200: OK'
        return f'400: {message[ERROR]}'
    raise ValueError


def main():
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('Порт должен быть в диапазоне 1024 - 65535')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_presence()
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        print(answer)
    except(ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера')


if __name__ == '__main__':
    main()
