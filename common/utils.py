import json

from common.variables import MAX_PACKAGE_LENCTH, ENCODING
from decos import log

@log
def get_message(client):
    encoded_response = client.recv(MAX_PACKAGE_LENCTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError

@log
def send_message(sock, message):
    if not isinstance(message, dict):
        raise TypeError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
