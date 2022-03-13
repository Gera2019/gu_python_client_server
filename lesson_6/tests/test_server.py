import unittest
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
from server import process_client_msg
from common.variables import DEFAULT_ADDRESS, DEFAULT_PORT, ACTION, ACCOUNT_NAME, PRESENCE, RESPONSE, USER, ERROR, TIME


class TestServer(unittest.TestCase):
    err_dict = {
        RESPONSE: 400,
        ERROR: 'Неправильный запрос'
    }
    ok_dict = {RESPONSE: 200}

    def test_200(self):
        msg = {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}
        msg_error = {}
        self.assertTrue((process_client_msg(msg), {RESPONSE: 200}), 'Обработка сообщения некорректна')

    def test_400(self):
        msg = {ACTION: PRESENCE}
        self.assertTrue((process_client_msg(msg), {RESPONSE: 400}), 'Неверная обработка исключительных ситуаций')

    def test_no_action(self):
        """Ошибка если нет действия"""
        self.assertEqual(process_client_msg(
          {TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_wrong_action(self):
        """Ошибка если неизвестное действие"""
        self.assertEqual(process_client_msg(
          {ACTION: 'Wrong', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_time(self):
        """Ошибка, если запрос не содержит штампа времени"""
        self.assertEqual(process_client_msg(
          {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_user(self):
        """Ошибка - нет пользователя"""
        self.assertEqual(process_client_msg(
          {ACTION: PRESENCE, TIME: '1.1'}), self.err_dict)

    def test_unknown_user(self):
        """Ошибка - не Guest"""
        self.assertEqual(process_client_msg(
          {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest1'}}), self.err_dict)

    def test_ok_check(self):
        """Корректный запрос"""
        self.assertEqual(process_client_msg(
          {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_dict)

if __name__ == '__main__':
    unittest.main()