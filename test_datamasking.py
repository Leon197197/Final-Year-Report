import unittest
from datamasking import DataMasking

class Test_DataMasking(unittest.TestCase):
    def setUp(self):
        pass

    def test_masking(self):
        str1 = "My account is 77443399, phone number 07752437830 and address is Flat 67, Room 1, Shackleton, Church Road, Edgbaston"
        str2 = DataMasking.masking(str1)
        print(f"DataMasking result is {str2}")
        self.assertNotEqual(str2,str1)

    def tearDown(self):
        pass
if __name__ == '__main__':
    unittest.main()