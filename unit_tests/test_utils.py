import json
import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.utils import send_message, get_message
from common.variables import ENCODING, TIME, ACTION, USER, ACCOUNT_NAME, PRESENCE, RESPONCE, ERROR


class TestSocket:

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.received_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestUtils(unittest.TestCase):
    test_dict_send = {
        ACTION: PRESENCE,
        TIME: 1111.11111,
        USER: {
            ACCOUNT_NAME: 'test'
        }
    }
    test_dict_recv_ok = {RESPONCE: 200}
    test_dict_recv_err = {RESPONCE: 400, ERROR: 'Bad request'}

    def test_send_message(self):
        test_socket = TestSocket(self.test_dict_send)
        send_message(test_socket, self.test_dict_send)
        self.assertEqual(test_socket.encoded_message, test_socket.received_message)

    def test_send_message_err(self):
        test_socket = TestSocket(self.test_dict_send)
        send_message(test_socket, self.test_dict_send)
        self.assertRaises(TypeError, send_message, test_socket, 'wrong_dictionary')

    def test_get_message(self):
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        self.assertEqual((get_message(test_sock_ok)), self.test_dict_recv_ok)

    def test_get_message_err(self):
        test_sock_err = TestSocket(self.test_dict_recv_err)
        self.assertEqual((get_message(test_sock_err)), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
