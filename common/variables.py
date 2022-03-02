import logging

DEFAULT_PORT = 7777

DEFAULT_IP_ADDRESS = '127.0.0.1'

MAX_CONNECTIONS = 5

MAX_PACKAGE_LENCTH = 1024

LOGGING_LEVEL = logging.DEBUG

ENCODING = 'utf-8'

ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'sender'

PRESENCE = 'presence'
RESPONCE = 'responce'
ERROR = 'error'
RESPONDEFAULT_IP_ADDRESS = 'respondefault_ip_address'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
RESPONSE_200 = {RESPONCE: 200}
EXIT = 'exit'
RESPONSE_400 = {
    RESPONCE: 400,
    ERROR: None}

DESTINATION = 'to'
