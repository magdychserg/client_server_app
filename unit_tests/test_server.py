import os
import sys
import unittest
from unittest.mock import patch

import server

sys.path.append(os.path.join(os.getcwd(), '..'))
from server import process_client_message
from common.variables import TIME, ACTION, USER, ACCOUNT_NAME, PRESENCE, RESPONCE, ERROR, RESPONDEFAULT_IP_ADDRESS


class TestServer(unittest.TestCase):
    err_dict = {
        RESPONDEFAULT_IP_ADDRESS: 400,
        ERROR: 'Bad request'
    }
    ok_dict = {RESPONCE: 200}

    def test_ok_check(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}),
                         self.ok_dict)

    def test_no_action(self):
        self.assertEqual(process_client_message({TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_wrong_action(self):
        self.assertEqual(process_client_message({ACTION: 'Wrong', TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}),
                         self.err_dict)

    def test_no_time(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_user(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, TIME: 1.1}), self.err_dict)

    def test_unknown_user(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest1'}}),
                         self.err_dict)

    @patch.object(sys, 'argv', ['server.py', '-p', 7777])
    def test_with_mock(self):
        # self.assertRaises(IndexError, server.main)
        self.assertEqual(server.main, 7777)


if __name__ == '__main__':
    unittest.main()
