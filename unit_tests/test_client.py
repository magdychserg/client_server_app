import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import TIME, ACTION, USER, ACCOUNT_NAME, PRESENCE, RESPONCE, ERROR
from client import create_presence, process_ans


class TestClient(unittest.TestCase):

    def test_def_presense(self):
        test = create_presence()
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_200_ans(self):
        self.assertEqual(process_ans({RESPONCE: 200}), '200: OK')

    def test_400_ans(self):
        self.assertEqual(process_ans({RESPONCE: 400, ERROR: 'Bad Request'}), '400: Bad Request')

    def test_no_response(self):
        self.assertRaises(ValueError, process_ans, ({ERROR: 'Bad request'}))


if __name__ == '__main__':
    unittest.main()
