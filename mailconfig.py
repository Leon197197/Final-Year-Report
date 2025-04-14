import configparser
import os
import psutil
import subprocess
from datasecurity import DataSecurity

# Read & Write the configure file
class MailConfig:
    config_file = None
    outlook_path = None
    dify_url = None
    analysis_api_key = None
    reply_api_key = None
    mail_account = None
    dbname = None
    dbuser = None
    dbpassword = None
    dbhost = None
    dbport = None
    filename_analysis = None
    filename_reply = None
    kb_analysis = None
    kb_reply = None

    # Read the content of config.ini
    @classmethod
    def read_config(cls):
        cls.config_file = configparser.ConfigParser()
        cls.config_file.read('config.ini')

        cls.outlook_path = cls.config_file.get('General', 'outlook_path')
        cls.dify_url = cls.config_file.get('General', 'dify_url')
        cls.analysis_api_key = cls.config_file.get('General', 'analysis_api_key')
        cls.reply_api_key = cls.config_file.get('General', 'reply_api_key')
        cls.mail_account = cls.config_file.get('General', 'mail_account')
        cls.filename_analysis = cls.config_file.get('General', 'kb_analysis')
        cls.filename_reply = cls.config_file.get('General', 'kb_reply')
        cls.kb_analysis = cls.read_file_content(cls.filename_analysis)
        cls.kb_reply = cls.read_file_content(cls.filename_reply)

        cls.dbname = cls.config_file.get('Database', 'dbname')
        cls.dbuser = cls.config_file.get('Database', 'dbuser')
        strpwd = cls.config_file.get('Database', 'password')
        #pwd=base64.b64decode(strpwd)
        cls.dbpassword = DataSecurity.decrypt_password(strpwd)
        cls.dbhost = cls.config_file.get('Database', 'dbhost')
        cls.dbport = cls.config_file.get('Database', 'dbport')

    # Write the content of config.ini
    @classmethod
    def write_config(cls):
        cls.config_file.set('General', 'outlook_path', cls.outlook_path)
        cls.config_file.set('General', 'kb_analysis', cls.filename_analysis)
        cls.config_file.set('General', 'analysis_api_key', cls.analysis_api_key)
        cls.config_file.set('Database', 'dbname', cls.dbname)
        cls.config_file.set('Database', 'dbuser', cls.dbuser)
        strpwd = DataSecurity.encrypt_password(cls.dbpassword)
        #strpwd=base64.b64encode(pwd).decode('utf-8')
        cls.config_file.set('Database', 'password', strpwd)
        cls.config_file.set('Database', 'dbhost', cls.dbhost)
        cls.config_file.set('Database', 'dbport', cls.dbport)
        with open('config.ini', 'w') as config_file:
            cls.config_file.write(config_file)

    # get the Outlook application is opened or not
    @classmethod
    def is_process_exist(cls,process_name):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if process_name in proc.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    # Open the Outlook application
    @classmethod
    def open_outlook(cls):
        if cls.config_file is None:
            cls.read_config()
        if not cls.is_process_exist('outlook.exe'):
            if os.path.exists(cls.outlook_path):
                subprocess.Popen(cls.outlook_path)
            else:
                print("Can't find Outlook.exe.")

    # Read the content of filename given
    @classmethod
    def read_file_content(cls,file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            print("Error read_file_content: FileNotFoundError")
        except Exception as e:
            print(f"Error read_file_content: {e}")
        else:
            return content


