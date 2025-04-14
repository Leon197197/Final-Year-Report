from mailllm import MailLLM
import win32com.client as win32
from mailconfig import MailConfig
from mailllm import MailLLM
from maildatabase import MailDatabase
from datamasking import DataMasking
import re
import pandas as pd

class MailHelper:
    def __init__(self):
        self.outlook = win32.Dispatch('Outlook.Application')
        namespace = self.outlook.GetNamespace('MAPI')
        self.root_folder = namespace.Folders.Item(MailConfig.mail_account)
        self.inbox_folder = namespace.GetDefaultFolder(6)  # 6--Inbox
        self.analysis_llm = MailLLM(MailConfig.dify_url,MailConfig.analysis_api_key)
        self.reply_llm = MailLLM(MailConfig.dify_url, MailConfig.reply_api_key)

    # Create folders in inbox
    def init_mail(self):
        self.check_mail_folder(self.inbox_folder, "1.Urgent", True)
        self.check_mail_folder(self.inbox_folder, "2.Moderate", True)
        return True

    def check_mail_folder(self, parent_folder, folder_name, is_created):
        try:
            subfolders = parent_folder.Folders
            for folder in subfolders:
                if folder.Name == folder_name:
                    return folder
            if not is_created: return None
            print(f"Folder '{folder_name}' is not exist, creating...")
            new_folder = parent_folder.Folders.Add(folder_name)
            return new_folder
        except Exception as e:
            print(f"Error --get_mail_folder: {str(e)}")
            return None


    # get folder by folder name
    def get_folder_by_name(self,folder_name):
        for folder in self.inbox_folder.Folders:
            if folder.Name == folder_name:
                return folder
            sub_folders = folder.Folders
            for sub_folder in sub_folders:
                if sub_folder.Name == folder_name:
                    return sub_folder
        return None

    # Delete forword message to get the lastest content in email
    def get_email_lastest_content(self,email_body):
        forwarded_pattern = r"(?:\n|\r\n)?(From:|Sent:|To:|Subject:).*"
        lastest_content = re.sub(forwarded_pattern, "", email_body, flags=re.DOTALL)
        return lastest_content

    #Classfy emails by calling LLM & knowledge base
    def classify_emails(self):
        messages = self.inbox_folder.Items
        messages.Sort("[ReceivedTime]", True)  # sort per time，True--desc
        for message in messages:
            try:
                if message.Unread:
                    str_content = self.get_email_lastest_content(message.body)
                    str_mail = f"Email Subject:{message.subject}; Email content:{str_content}"
                    str_masking = DataMasking.masking(str_mail)
                    factor_sentiment,factor_time,llm_result = self.get_emergency_level(str_masking)
                    level = max(factor_sentiment,factor_time)
                    target_folder_name = ""
                    if level == '3':
                        target_folder_name="1.Urgent"
                    elif level == '2':
                        target_folder_name = "2.Moderate"
                    if target_folder_name == "": continue

                    message.Move(self.get_folder_by_name(target_folder_name))
                    MailDatabase.insert_logs_analysis(llm_result+'='+level, target_folder_name,message.ReceivedTime, message.SenderEmailAddress, MailHelper.truncate_string(message.Subject, 200), self.truncate_string(message.body, 1000),level,factor_sentiment,factor_time)
            except Exception as e:
                print(f"Error --classify_emails: '{message.Subject}': {e}")

    # Get email emergency level from LLM
    def get_emergency_level(self,str_mail):
        str1 = ', '.join(MailDatabase.array_sentiment)
        str_sentiment = self.analysis_llm.ask_analysis_llm(str_mail,str1)
        llm_result=""
        str2 = ', '.join(MailDatabase.array_time)
        str_time = self.analysis_llm.ask_analysis_llm(str_mail, str2)
        factor_sentiment = 1
        factor_time = 1
        row = 0
        for item in MailDatabase.array_sentiment:
            if item in str_sentiment:
                factor_sentiment = MailDatabase.array_sentiment_factor[row]
                llm_result=item
                break
            row=row+1

        row = 0
        for item in MailDatabase.array_time:
            if item in str_time:
                factor_time =MailDatabase.array_time_factor[row]
                llm_result=llm_result+','+item
                break
            row = row + 1
        return factor_sentiment,factor_time,llm_result

    # Get substring to cut too large string
    @classmethod
    def truncate_string(cls,s,n):
        return s[:n] if len(s) > n else s

    # Send email per parameters
    def send_email(self,str_subject, str_body, recipients):
        new_mail = self.outlook.CreateItem(0)
        new_mail.Subject = str_subject
        new_mail.Body = str_body
        new_mail.To = recipients
        new_mail.Send()

    # send test emails
    def send_test_LLMs(self):
        data = pd.read_csv("testdata.csv")
        results = {'sn': [], 'email': [], 'factor_sentiment': [], 'factor_time': [], 'llm_sentiment': [], 'llm_time': []}
        for row in range(len(data)):
            value=data.iloc[row, 1]
            factor_sentiment,factor_time,llm_result = self.get_emergency_level(value)
            print(f"SN={row+1},{factor_sentiment},{factor_time},{llm_result}")
            results['sn'].append(row+1)
            results['email'].append(value)
            results['factor_sentiment'].append(factor_sentiment)
            results['factor_time'].append(factor_time)
            llm = llm_result.split(",")
            results['llm_sentiment'].append(llm[0])
            results['llm_time'].append(llm[1])
        df = pd.DataFrame(results)
        filename="result_deepseek.csv"
        df.to_csv(filename, index=False, encoding="utf-8")
        print(f"Results saved in {filename}")

    # send test emails
    def send_test_mails(self):
        recipients = "leon.en.lee@outlook.com"
        self.send_email("How to borrow a laptop",
                   "My laptop was broken, how can I get a laptop in campus as soon as possible", recipients)
        self.send_email("How to borrow books from library",
                   "Please tell me how to borrow books from library as soon as possible,Please tell me how to borrow books from library as soon as possible,Please tell me how to borrow books from library as soon as possible,Please tell me how to borrow books from library as soon as possiblePlease tell me how to borrow books from library as soon as possiblePlease tell me how to borrow books from library as soon as possiblePlease tell me how to borrow books from library as soon as possible,Please tell me how to borrow books from library as soon as possible", recipients)
        self.send_email("terrible service",
                   "I complained about the poor service provided by the library", recipients)
        self.send_email("Happy New Year",
                   "Happy New Year, on behalf of the school, I wish every student a happy New Year", recipients)
        self.send_email("Stop making noice",
                   "I am very furious about the noise at your house at night. Please stop making noise", recipients)
        self.send_email("Stop making noice immediately",
                   "I am very furious about the noise at your house at night. Please stop making noise immediately", recipients)

