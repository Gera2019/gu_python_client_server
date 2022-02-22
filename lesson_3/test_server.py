import unittest
from server import response_prepare

class TestServer(unittest.TestCase):

  def test_response_prepare_200(self):
      msg = {'action': 'presence', 'user':{'account_name': 'Gueset'}}
      msg_error = {}
      self.assertTrue((response_prepare(msg), {'response': 200}), 'Обработка сообщения некорректна')

  def test_response_prepare_400(self):
      msg = {'action': 'presence'}
      self.assertTrue((response_prepare(msg), {'response': 400}), 'Неверная обработка исключительных ситуаций')

if __name__ == '__main__':
    unittest.main()