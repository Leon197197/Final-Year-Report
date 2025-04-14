import wx
import wx.adv
import wx.grid
import threading
from pathlib import Path
import time
from maildatabase import MailDatabase
from mailhelper import MailHelper
from mailconfig import MailConfig
from datetime import datetime

class MailApp(wx.Frame):
    def __init__(self, *args, **kw):
        super(MailApp, self).__init__(*args, **kw)
        self.font_title = wx.Font(16, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_header = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_label = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.panelcolor = wx.Colour(235, 246, 249)
        self.backgroundcolor=wx.Colour(235, 246, 249)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.CreateStatusBar(1)
        self.SetStatusText("Welcome to use Outlook AI Helper", 0)
        self.create_left_panel()
        self.create_right_panel()
        # Layout design
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer.Add(self.left_panel, 0, flag=wx.EXPAND)
        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_sizer.Add(self.right_panel0, 1, flag=wx.EXPAND)
        #self.panel_sizer.Add(self.right_panel1, 1, flag=wx.EXPAND)
        self.panel_sizer.Add(self.right_panel2, 1, flag=wx.EXPAND)
        #self.panel_sizer.Add(self.right_panel3, 1, flag=wx.EXPAND)
        self.panel_sizer.Add(self.right_panel4, 1, flag=wx.EXPAND)
        self.panel_sizer.Add(self.right_panel5, 1, flag=wx.EXPAND)
        self.main_sizer.Add(self.panel_sizer, 1, flag=wx.EXPAND)
        self.SetSizer(self.main_sizer)
        icon_mail = wx.Icon('mail.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon_mail)

        self.thread = threading.Thread(target=self.run_background_task)
        self.thread.daemon = True
        self.thread.start()
        self.Center()
        self.Layout()

    # Triggered by the event of app window close is triggered
    def on_close(self,event):
        MailDatabase.disconnect_db()
        self.Destroy()

    # the thread of scanning outlook inbox
    def run_background_task(self):
        while True:
            time.sleep(6000)
            self.execute_task()

    def execute_task(self):
        wx.CallAfter(self.update_ui)

    # Scanning outlook inbox and update status text
    def update_ui(self):
        self.SetStatusText(f"Latest email analysis time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Create the left panel of app window
    def create_left_panel(self):
        self.left_panel = wx.Panel(self)

        self.left_panel.SetBackgroundColour(self.backgroundcolor)
        label = wx.StaticText(self.left_panel, label="      Homepage", pos=(20, 20))
        label.SetFont(self.font_title)
        self.options_list = wx.ListCtrl(self.left_panel, pos=(20, 20), size=(220, 200), style=wx.LC_REPORT|wx.LC_NO_HEADER | wx.NO_BORDER)
        self.options_list.InsertColumn(0, "item", width=220)
        self.options_list.SetFont(self.font_header)
        icon_size = (24, 48)
        self.icon_bundle = wx.ImageList(*icon_size)
        icon0 = wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_CMN_DIALOG, icon_size)
        icon2 = wx.ArtProvider.GetBitmap(wx.ART_HELP_FOLDER, wx.ART_CMN_DIALOG, icon_size)
        icon4 = wx.ArtProvider.GetBitmap(wx.ART_EDIT, wx.ART_CMN_DIALOG, icon_size)
        icon5 = wx.ArtProvider.GetBitmap(wx.ART_ADD_BOOKMARK, wx.ART_CMN_DIALOG, icon_size)
        self.icon_bundle.Add(icon0)
        self.icon_bundle.Add(icon2)
        self.icon_bundle.Add(icon4)
        self.icon_bundle.Add(icon5)        
        self.options_list.AssignImageList(self.icon_bundle, wx.IMAGE_LIST_SMALL)

        self.options_list.InsertItem(0, "Email analysis logs", 0)
        self.options_list.InsertItem(1, "Analysis knowledge base", 1)
        self.options_list.InsertItem(2, "Urgency Level", 2)
        self.options_list.InsertItem(3, "System settings", 3)
        self.options_list.SetBackgroundColour(self.left_panel.GetBackgroundColour())

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(label, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        left_sizer.Add(self.options_list, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        self.left_panel.SetSizer(left_sizer)

        # bind events
        self.options_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_option_selected)


    # Create the right panel of app window
    def create_right_panel(self):

        self.create_right_panel0()
        self.create_right_panel2()
        self.create_right_panel4()
        self.create_right_panel5()

        self.right_panel0.SetBackgroundColour(self.backgroundcolor)
        self.right_panel2.SetBackgroundColour(self.backgroundcolor)
        self.right_panel4.SetBackgroundColour(self.backgroundcolor)
        self.right_panel5.SetBackgroundColour(self.backgroundcolor)
        self.list_analysis.SetLabelBackgroundColour(self.backgroundcolor)
        self.list_sentiment.SetLabelBackgroundColour(self.backgroundcolor)
        self.list_time.SetLabelBackgroundColour(self.backgroundcolor)

        self.right_panel0.Show()
        #self.right_panel1.Hide()
        self.right_panel2.Hide()
        #self.right_panel3.Hide()
        self.right_panel4.Hide()
        self.right_panel5.Hide()


    def create_right_panel0(self):
        #panel0:  Email analysis logs
        self.right_panel0 = wx.Panel(self)
        self.right_panel0_top = wx.Panel(self.right_panel0)
        self.lable_date0 = wx.StaticText(self.right_panel0_top, label=f"Email analysis logs of {datetime.now().strftime('%Y-%m-%d')}, Other records please select date: ")
        self.lable_date0.SetFont(self.font_header)
        self.date_picker0 = wx.adv.DatePickerCtrl(self.right_panel0_top, style=wx.adv.DP_DROPDOWN, size=(100, 20))
        self.date_picker0.Bind(wx.adv.EVT_DATE_CHANGED, self.on_date_changed0)
        right_panel0_top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_panel0_top_sizer.Add(self.lable_date0, 0, wx.ALL, 5)
        right_panel0_top_sizer.Add(self.date_picker0, 0, wx.ALL, 5)
        self.right_panel0_top.SetSizer(right_panel0_top_sizer)
        self.list_analysis = wx.grid.Grid(self.right_panel0, style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES | wx.LC_SORT_ASCENDING, pos=(10, 10), size=(900, 300))
        self.list_analysis.SetRowLabelSize(50)
        #self.list_log.SetLabelBackgroundColour(wx.Colour(240, 240, 240))
        self.list_analysis.SetGridLineColour(wx.Colour(255, 255, 255))
        self.list_analysis.CreateGrid(21, 8)
        self.list_analysis.SetColLabelValue(0, 'ID')
        self.list_analysis.SetColLabelValue(1, 'Analysis Date')
        self.list_analysis.SetColLabelValue(2, 'LLM Result')
        self.list_analysis.SetColLabelValue(3, 'Classified')
        self.list_analysis.SetColLabelValue(4, 'ReceivedTime')
        self.list_analysis.SetColLabelValue(5, 'Sender')
        self.list_analysis.SetColLabelValue(6, 'Subject')
        self.list_analysis.SetColLabelValue(7, 'Content')
        self.list_analysis.SetColSize(0,30)
        self.list_analysis.SetColSize(1,150)
        self.list_analysis.SetColSize(2,100)
        self.list_analysis.SetColSize(3,100)
        self.list_analysis.SetColSize(4,200)
        self.list_analysis.SetColSize(5,200)
        self.list_analysis.SetColSize(6,200)
        self.list_analysis.SetColSize(7,200)
        right_panel0_sizer = wx.BoxSizer(wx.VERTICAL)
        right_panel0_sizer.Add(self.right_panel0_top, 0, wx.ALL, 5)
        right_panel0_sizer.Add(self.list_analysis, 1, wx.EXPAND | wx.ALL, 5)
        self.right_panel0.SetSizer(right_panel0_sizer)
        self.on_date_changed0(self.date_picker0)

    # panel2: Analysis knowledge base
    def create_right_panel2(self):
        self.right_panel2 = wx.Panel(self)
        self.right_panel2_top = wx.Panel(self.right_panel2)
        self.label_date2 = wx.StaticText(self.right_panel2_top, label=f"Knowledge base for email analysis: ")
        self.label_date2.SetFont(self.font_header)
        right_panel2_top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_panel2_top_sizer.Add(self.label_date2, 0, wx.ALL, 5)
        self.right_panel2_top.SetSizer(right_panel2_top_sizer)
        self.text_analysis = wx.TextCtrl(self.right_panel2, style=wx.TE_MULTILINE | wx.TE_WORDWRAP, size=(300, 200))
        right_panel2_sizer = wx.BoxSizer(wx.VERTICAL)
        right_panel2_sizer.Add(self.right_panel2_top, 0, wx.ALL, 5)
        right_panel2_sizer.Add(self.text_analysis, 1, wx.EXPAND | wx.ALL, 5)
        self.right_panel2.SetSizer(right_panel2_sizer)
        self.text_analysis.SetValue(MailConfig.kb_analysis)

    #panel4: Email Urgency Level
    def create_right_panel4(self):
        self.right_panel4 = wx.Panel(self)
        #self.right_panel4_top = wx.Panel(self.right_panel4)
        label_sentiment = wx.StaticText(self.right_panel4, label=f"Email sentiment factor setting: ")
        label_sentiment.SetFont(self.font_header)
        self.list_sentiment = wx.grid.Grid(self.right_panel4, style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES|wx.LC_SORT_ASCENDING, pos=(10, 10), size=(900, 280))
        self.list_sentiment.SetRowLabelSize(50)
        #self.list_sentiment.SetLabelBackgroundColour(wx.Colour(240, 240, 240))
        self.list_sentiment.SetGridLineColour(wx.Colour(255, 255, 255))
        self.list_sentiment.CreateGrid(14, 4)
        self.list_sentiment.SetColLabelValue(0, 'ID')
        self.list_sentiment.SetColLabelValue(1, 'Sentiment Class')
        self.list_sentiment.SetColLabelValue(2, 'Factor Value')
        self.list_sentiment.SetColLabelValue(3, ' ')
        self.list_sentiment.SetColSize(0,100)
        self.list_sentiment.SetColSize(1,300)
        self.list_sentiment.SetColSize(2,200)
        self.list_sentiment.SetColSize(3, 100)
        self.set_column_readonly(self.list_sentiment,0)
        self.set_column_readonly(self.list_sentiment, 1)
        label_time = wx.StaticText(self.right_panel4, label=f"Email time factor setting: ")
        label_time.SetFont(self.font_header)
        self.list_time = wx.grid.Grid(self.right_panel4, style=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES|wx.LC_SORT_ASCENDING, pos=(10, 10), size=(900, 100))
        self.list_time.SetRowLabelSize(50)
        #self.list_time.SetLabelBackgroundColour(wx.Colour(240, 240, 240))
        self.list_time.SetGridLineColour(wx.Colour(255, 255, 255))
        self.list_time.CreateGrid(3, 4)
        self.list_time.SetColLabelValue(0, 'ID')
        self.list_time.SetColLabelValue(1, 'Time Class')
        self.list_time.SetColLabelValue(2, 'Factor Value')
        self.list_time.SetColLabelValue(3, ' ')
        self.list_time.SetColSize(0,100)
        self.list_time.SetColSize(1,300)
        self.list_time.SetColSize(2,200)
        self.list_time.SetColSize(3, 100)
        self.set_column_readonly(self.list_time,0)
        self.set_column_readonly(self.list_time, 1)
        self.button_cancel_factor = wx.Button(self.right_panel4, label="Reset", pos=(600, 50), size=(120, 30))
        self.button_cancel_factor.Bind(wx.EVT_BUTTON, self.on_button_cancel_factor_click)
        self.button_save_factor = wx.Button(self.right_panel4, label="Save", pos=(600, 50), size=(120, 30))
        self.button_save_factor.Bind(wx.EVT_BUTTON, self.on_button_save_factor_click)
        right_panel4_sizer = wx.BoxSizer(wx.VERTICAL)
        right_panel4_sizer.Add(label_sentiment, 0, wx.ALL, 5)
        right_panel4_sizer.Add(self.list_sentiment, 0, wx.ALL, 5)
        right_panel4_sizer.Add(label_time, 0, wx.ALL, 5)
        right_panel4_sizer.Add(self.list_time, 0, wx.ALL, 5)

        right_panel4_sizer.Add(wx.StaticLine(self.right_panel4), 0, wx.ALL|wx.EXPAND, 5)
        sizer_right = wx.BoxSizer(wx.HORIZONTAL)
        sizer_right.Add(self.button_cancel_factor, 0, wx.ALL, 10)
        sizer_right.Add(self.button_save_factor, 0, wx.ALL, 10)
        sizer_right.AddSpacer(100)

        right_panel4_sizer.Add(sizer_right, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        self.right_panel4.SetSizer(right_panel4_sizer)
        self.right_panel4.SetBackgroundColour(self.panelcolor)
        MailDatabase.query_sentiment_factor(self.list_sentiment)
        MailDatabase.query_time_factor(self.list_time)

    # Triggered by button 'cancel' click to cancel update and refresh data from database
    def on_button_cancel_factor_click(self, event):
        MailDatabase.query_sentiment_factor(self.list_sentiment)
        MailDatabase.query_time_factor(self.list_time)

    # Triggered by button 'save' click to save factor data to database
    def on_button_save_factor_click(self, event):
        MailDatabase.update_sentiment_factor(self.list_sentiment)
        MailDatabase.update_time_factor(self.list_time)

    # set grid column readonly
    def set_column_readonly(self, dataset, col):
        for row in range(dataset.GetNumberRows()):
            dataset.SetReadOnly(row, col)

    # panel5: Settings
    def create_right_panel5(self):
        self.right_panel5 = wx.Panel(self)
        self.right_panel5.SetFont(self.font_label)

        general_label = wx.StaticText(self.right_panel5, label=f"General setting: ")
        database_label = wx.StaticText(self.right_panel5, label=f"Database setting: ")
        general_label.SetFont(self.font_header)
        database_label.SetFont(self.font_header)
        line1 = wx.StaticLine(self.right_panel5)
        line2 = wx.StaticLine(self.right_panel5)
        line3 = wx.StaticLine(self.right_panel5)
        right_panel5_top = wx.Panel(self.right_panel5)
        right_panel5_center = wx.Panel(self.right_panel5)
        right_panel5_bottom = wx.Panel(self.right_panel5)
        right_panel5_sizer = wx.BoxSizer(wx.VERTICAL)
        #right_panel5_sizer.AddStretchSpacer(1)
        right_panel5_sizer.Add(general_label, 0, wx.ALL, 5)
        right_panel5_sizer.Add(line1, 0, wx.ALL|wx.EXPAND, 5)
        right_panel5_sizer.Add(right_panel5_top, 0, wx.ALL|wx.EXPAND, 5)
        right_panel5_sizer.Add(database_label, 0, wx.ALL, 5)
        right_panel5_sizer.Add(line2, 0, wx.ALL|wx.EXPAND, 5)
        right_panel5_sizer.Add(right_panel5_center, 0, wx.ALL|wx.EXPAND, 5)
        right_panel5_sizer.Add(line3, 0, wx.ALL | wx.EXPAND, 5)
        right_panel5_sizer.Add(right_panel5_bottom, 0, wx.EXPAND, 5)
        self.right_panel5.SetSizer(right_panel5_sizer)

        bitmap_fileopen = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16, 16))
        self.path_label = wx.StaticText(right_panel5_top, label="Outlook application path: ")
        self.path_input = wx.TextCtrl(right_panel5_top, size=(400, 25))
        self.kb_analysis_label = wx.StaticText(right_panel5_top, label="Analysis knowledge base file: ")
        self.kb_analysis_input = wx.TextCtrl(right_panel5_top, size=(400, 25))
        self.api_key_label = wx.StaticText(right_panel5_top, label="LLM api key: ")
        self.api_key_input = wx.TextCtrl(right_panel5_top, size=(400, 25))
        self.path_button = wx.BitmapButton(right_panel5_top, bitmap=bitmap_fileopen, pos=(50, 50))
        self.kb_analysis_button = wx.BitmapButton(right_panel5_top, bitmap=bitmap_fileopen, pos=(50, 50))

        right_panel5_top_sizer = wx.GridBagSizer(6, 6)
        right_panel5_top_sizer.Add(self.path_label, pos=(0, 1), span=(1, 1), flag=wx.EXPAND, border=5)
        right_panel5_top_sizer.Add(self.path_input, pos=(1, 1), span=(1, 1), flag=wx.EXPAND, border=5)
        right_panel5_top_sizer.Add(self.path_button, pos=(1, 2), span=(1, 1), flag=wx.EXPAND, border=5)
        right_panel5_top_sizer.Add(self.kb_analysis_label, pos=(2, 1), span=(1, 1), flag=wx.EXPAND, border=5)
        right_panel5_top_sizer.Add(self.kb_analysis_input, pos=(3, 1), span=(1, 1), flag=wx.EXPAND, border=5)
        right_panel5_top_sizer.Add(self.kb_analysis_button, pos=(3, 2), span=(1, 1), flag=wx.EXPAND, border=5)
        right_panel5_top_sizer.Add(self.api_key_label, pos=(4, 1), span=(1, 1), flag=wx.EXPAND, border=5)
        right_panel5_top_sizer.Add(self.api_key_input, pos=(5, 1), span=(1, 1), flag=wx.EXPAND, border=5)
        right_panel5_top.SetSizer(right_panel5_top_sizer)
        right_panel5_top.SetBackgroundColour(self.panelcolor)

        self.dbname_label = wx.StaticText(right_panel5_center, label="Database name: ")
        self.dbname_input = wx.TextCtrl(right_panel5_center,  size=(200, 30))
        self.dbuser_label = wx.StaticText(right_panel5_center, label="Database user: ")
        self.dbuser_input = wx.TextCtrl(right_panel5_center, size=(200, 30))
        self.dbpassword_label = wx.StaticText(right_panel5_center, label="Database password: ")
        self.dbpassword_input = wx.TextCtrl(right_panel5_center, style=wx.TE_PASSWORD, size=(200, 30))
        self.dbhost_label = wx.StaticText(right_panel5_center, label="Database host: ")
        self.dbhost_input = wx.TextCtrl(right_panel5_center, size=(200, 30))
        self.dbport_label = wx.StaticText(right_panel5_center, label="Database port: ")
        self.dbport_input = wx.TextCtrl(right_panel5_center, size=(200, 30))
        self.button_test = wx.Button(right_panel5_center, label="Test",size=(100, 30))
        right_panel5_center_sizer = wx.GridBagSizer(6, 6)
        right_panel5_center_sizer.Add(self.dbname_label, pos=(0, 1), span=(1, 1), flag=wx.ALIGN_RIGHT, border=5)
        right_panel5_center_sizer.Add(self.dbname_input, pos=(0, 2), span=(1, 1), flag=wx.EXPAND, border=5)
        right_panel5_center_sizer.Add(self.dbuser_label, pos=(1, 1), span=(1, 1), flag=wx.ALIGN_RIGHT, border=5)
        right_panel5_center_sizer.Add(self.dbuser_input, pos=(1, 2), span=(1, 1), flag=wx.EXPAND, border=5)
        right_panel5_center_sizer.Add(self.dbpassword_label, pos=(2, 1), span=(1, 1), flag=wx.ALIGN_RIGHT, border=5)
        right_panel5_center_sizer.Add(self.dbpassword_input, pos=(2, 2), span=(1, 1), flag=wx.EXPAND, border=5)
        right_panel5_center_sizer.Add(self.dbhost_label, pos=(3, 1), span=(1, 1), flag=wx.ALIGN_RIGHT, border=5)
        right_panel5_center_sizer.Add(self.dbhost_input, pos=(3, 2), span=(1, 1), flag=wx.EXPAND, border=5)
        right_panel5_center_sizer.Add(self.dbport_label, pos=(4, 1), span=(1, 1), flag=wx.ALIGN_RIGHT, border=5)
        right_panel5_center_sizer.Add(self.dbport_input, pos=(4, 2), span=(1, 1), flag=wx.EXPAND, border=5)
        right_panel5_center_sizer.Add(self.button_test, pos=(4, 3), span=(1, 1), flag=wx.EXPAND, border=5)
        right_panel5_center.SetSizerAndFit(right_panel5_center_sizer)
        right_panel5_center.SetBackgroundColour(self.panelcolor)

        self.path_input.SetValue(MailConfig.outlook_path)
        self.kb_analysis_input.SetValue(MailConfig.filename_analysis)
        self.api_key_input.SetValue(MailConfig.analysis_api_key)
        self.dbname_input.SetValue(MailConfig.dbname)
        self.dbuser_input.SetValue(MailConfig.dbuser)
        self.dbpassword_input.SetValue(MailConfig.dbpassword)
        self.dbhost_input.SetValue(MailConfig.dbhost)
        self.dbport_input.SetValue(MailConfig.dbport)

        self.button_save_config = wx.Button(right_panel5_bottom, label="Save", pos=(600, 5), size=(120, 30))

        self.path_button.Bind(wx.EVT_BUTTON,lambda event: self.on_select_file(event, self.path_input))
        self.kb_analysis_button.Bind(wx.EVT_BUTTON, lambda event: self.on_select_file(event, self.kb_analysis_input))
        #self.kb_reply_button.Bind(wx.EVT_BUTTON, lambda event: self.on_select_file(event, self.api_key_input))
        self.button_test.Bind(wx.EVT_BUTTON, self.on_button_test_click)
        self.button_save_config.Bind(wx.EVT_BUTTON, self.on_button_save_config_click)

        self.button_test_mail = wx.Button(right_panel5_bottom, label="Send test mails", pos=(5, 5), size=(120, 30))
        self.button_test_LLMs = wx.Button(right_panel5_bottom, label="Test LLMs", pos=(350, 5), size=(120, 30))
        self.button_test_classfication = wx.Button(right_panel5_bottom, label="Test Classfication", pos=(150, 5),
                                                   size=(120, 30))
        self.button_test_mail.Bind(wx.EVT_BUTTON, self.on_button_test_mail_click)
        self.button_test_LLMs.Bind(wx.EVT_BUTTON, self.on_button_test_LLMs_click)
        self.button_test_classfication.Bind(wx.EVT_BUTTON, self.on_button_test_classfication_click)

    def on_button_test_mail_click(self, event):
        mailhelper.send_test_mails()
    def on_button_test_LLMs_click(self, event):
        mailhelper.send_test_LLMs()
    def on_button_test_classfication_click(self, event):
        mailhelper.classify_emails()
        self.on_date_changed0(self.date_picker0)

    def on_select_file(self, event, text_ctrl):
        path = Path(text_ctrl.GetValue())
        directory = path.parent
        if str(directory) ==".":
            directory = Path(__file__).parent
        file_dialog = wx.FileDialog(self, "Choose a file", defaultDir=str(directory),wildcard="*.*", style=wx.FD_OPEN)
        if file_dialog.ShowModal() == wx.ID_OK:
            file_path = file_dialog.GetPath()
            text_ctrl.SetValue(file_path)
        file_dialog.Destroy()

    # Triggered by the event of date_picker0 changed date
    def on_date_changed0(self, event):
        # Retrieve the selected date
        selected_date0 = self.date_picker0.GetValue()
        self.list_analysis.ClearGrid()
        MailDatabase.query_logs_analysis(self.list_analysis, selected_date0)
        self.lable_date0.SetLabel(f"Email analysis logs of {selected_date0.Format("%Y-%m-%d")}, Other records please select date: ")

    # Triggered by button 'test' click to test database connect
    def on_button_test_click(self, event):
        isconnected,err=MailDatabase.test_connect(self.dbname_input.GetValue(),self.dbuser_input.GetValue(),self.dbpassword_input.GetValue(),self.dbhost_input.GetValue(),self.dbport_input.GetValue() )
        if isconnected:
            wx.MessageBox("Successfully connected database.", "Test database connect", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox(f"Failed to connect database: {err}", "Test database connect", wx.OK | wx.ICON_ERROR)

    # Triggered by button 'save' click to save config
    def on_button_save_config_click(self, event):
        MailConfig.outlook_path = self.path_input.GetValue()
        MailConfig.filename_analysis = self.kb_analysis_input.GetValue()
        MailConfig.analysis_api_key = self.api_key_input.GetValue()
        MailConfig.dbname = self.dbname_input.GetValue()
        MailConfig.dbuser =  self.dbuser_input.GetValue()
        MailConfig.dbpassword = self.dbpassword_input.GetValue()
        MailConfig.dbhost = self.dbhost_input.GetValue()
        MailConfig.dbport = self.dbport_input.GetValue()
        MailConfig.write_config()

    # Triggered by the event of the left list is clicked
    def on_option_selected(self, event):
        index = event.GetIndex()
        if index == 0:
            self.right_panel0.Show()
            #self.right_panel1.Hide()
            self.right_panel2.Hide()
            #self.right_panel3.Hide()
            self.right_panel4.Hide()
            self.right_panel5.Hide()
        elif index == 1:
            self.right_panel0.Hide()
            #self.right_panel1.Hide()
            self.right_panel2.Show()
            self.right_panel4.Hide()
            self.right_panel5.Hide()
        elif index == 2:
            self.right_panel0.Hide()
            self.right_panel2.Hide()
            self.right_panel4.Show()
            self.right_panel5.Hide()
        elif index == 3:
            self.right_panel0.Hide()
            self.right_panel2.Hide()
            self.right_panel4.Hide()
            self.right_panel5.Show()
        self.Layout()

app = wx.App(False)
MailConfig.read_config()
dbconnect,str=MailDatabase.connect_db()
if dbconnect is None:
    wx.MessageBox(f"Failed to connect database: {str}", "database connect", wx.OK | wx.ICON_ERROR)

MailConfig.open_outlook()
mailhelper = MailHelper()
mailhelper.init_mail()
frame = MailApp(None, title="Outlook AI Helper", size=(1050, 600))
frame.Show(True)
app.MainLoop()