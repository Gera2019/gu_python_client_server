import os
import sys
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from client import process_client_msg, process_server_msg
from common.utils import get_message
from common.variables import DEFAULT_ADDRESS, DEFAULT_PORT, ACTION, ACCOUNT_NAME, PRESENCE, RESPONSE, USER, ERROR, TIME

class TestClient(unittest.TestCase):

  def test_dict(self):
      self.assertTrue(isinstance(process_client_msg('Guest'), dict), 'Результат не является словарем')

  def test_def_presense(self):
      """Тест коректного запроса"""
      test = msg_prepare()
      test[TIME] = 1.1  # время необходимо приравнять принудительно
      # иначе тест никогда не будет пройден
      self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

  def test_200_ans(self):
      """Тест корректтного разбора ответа 200"""
      self.assertEqual(process_server_msg({RESPONSE: 200}), '200 : OK')

  def test_400_ans(self):
      """Тест корректного разбора 400"""
      self.assertEqual(process_server_msg({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')


if __name__ == '__main__':
    unittest.main()