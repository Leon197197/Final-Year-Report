import unittest
from mailhelper import MailHelper
from mailconfig import MailConfig

class Test_MailHelper(unittest.TestCase):
    def setUp(self):
        MailConfig.read_config()
        self.mailhelper = MailHelper()

    def test_init_mail(self):
        self.assertTrue(self.mailhelper.init_mail())

    def test_check_mail_folder(self):
        self.assertTrue(self.mailhelper.check_mail_folder(self.mailhelper.inbox_folder, "1.Urgent", True))

    def test_get_folder_by_name(self):
        self.assertEqual(self.mailhelper.get_folder_by_name("1.Urgent"), '1.Urgent')

    def tearDown(self):
        pass
if __name__ == '__main__':
    unittest.main()