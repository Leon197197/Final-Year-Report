import unittest
from datasecurity import DataSecurity

class Test_DataSecurity(unittest.TestCase):
    def setUp(self):
        pass

    def test_encrypt_password(self):
         self.assertTrue(DataSecurity.encrypt_password("Test123") != 'Test123')

    def test_decrypt_password(self):
         str = DataSecurity.encrypt_password("Test123")
         self.assertEqual(DataSecurity.decrypt_password(str), 'Test123')

    def tearDown(self):
        pass
if __name__ == '__main__':
    unittest.main()