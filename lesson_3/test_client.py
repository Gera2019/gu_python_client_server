import unittest
from client import msg_prepare
import time

class TestClient(unittest.TestCase):

  def test_message_prepare(self):
      self.assertTrue(isinstance(msg_prepare('Guest'), dict), 'Результат не является словарем')


if __name__ == '__main__':
    unittest.main()