import json
from socket import socket, SOL_SOCKET, SO_REUSEADDR
import sys
import socket
from common.utils import get_message, send_message
from common.variables import MAX_CONNECTIONS, ACTION, TIME, USER, ACCOUNT_NAME, PRESENCE, RESPONCE, \
    RESPONDEFAULT_IP_ADDRESS, ERROR, DEFAULT_PORT


def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message and message[USER][
        ACCOUNT_NAME] == 'Guest':
        return {RESPONCE: 200}
    return {
        RESPONDEFAULT_IP_ADDRESS: 400,
        ERROR: 'Bad request'
    }


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После -р необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        print('номер порта в пределах от 1024 до 65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''
    except IndexError:
        print(' После -а необходимо указать адрес')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято неккоректное сообщение')
            client.close()


if __name__ == '__main__':
    main()
