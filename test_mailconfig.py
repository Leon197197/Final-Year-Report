import unittest
from mailconfig import MailConfig

class Test_MailConfig(unittest.TestCase):
    def setUp(self):
        pass

    def test_read_config(self):
        MailConfig.read_config()
        self.assertEqual(MailConfig.dbport, '5433')

    def test_write_config(self):
        MailConfig.dbport ='5555'
        MailConfig.write_config()
        MailConfig.read_config()
        self.assertEqual(MailConfig.dbport, '5555')
        MailConfig.dbport ='5433'
        MailConfig.write_config()

    def tearDown(self):
        pass
if __name__ == '__main__':
    unittest.main()