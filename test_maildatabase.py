import unittest
from maildatabase import MailDatabase
from mailconfig import MailConfig
import wx
import wx.adv
import wx.grid


class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        self.SetTitle("wx.Grid Example")
        self.SetSize((600, 400))
        panel = wx.Panel(self)
        self.list_time = wx.grid.Grid(panel)
        self.list_time.SetRowLabelSize(50)
        #self.list_time.SetLabelBackgroundColour(wx.Colour(240, 240, 240))
        self.list_time.SetGridLineColour(wx.Colour(255, 255, 255))
        self.list_time.CreateGrid(3, 4)
        self.list_time.SetColLabelValue(0, 'ID')
        self.list_time.SetColLabelValue(1, 'Time Class')
        self.list_time.SetColLabelValue(2, 'Factor Value')
        self.list_time.SetColLabelValue(3, ' ')

app = wx.App(False)
frame = MyFrame(None, title="Outlook AI Helper", size=(1050, 600))

class Test_MailDatabase(unittest.TestCase):
    def setUp(self):
        MailConfig.read_config()

    def test_connect_db(self):
        s,err = MailDatabase.connect_db()
        self.assertEqual(err, "OK")

    def test_disconnect_db(self):
        self.assertEqual(MailDatabase.disconnect_db(), None)

    def test_test_connect(self):
        self.assertTrue(MailDatabase.test_connect("dify","test","123123","localhost","5433"))

    def test_query_time_factor(self):
        self.assertEqual(MailDatabase.query_time_factor(frame.list_time),3)

    def test_update_time_factor(self):
        self.assertEqual(MailDatabase.update_time_factor(frame.list_time),3)

    def tearDown(self):
        MailDatabase.disconnect_db()

if __name__ == '__main__':
    unittest.main()