import psycopg2
from psycopg2 import OperationalError
import wx
from mailconfig import MailConfig

class MailDatabase:
    connect = None
    array_sentiment = []
    array_sentiment_factor = []
    array_time = []
    array_time_factor = []
    # Connect the dify database
    @classmethod
    def connect_db(cls):
        err='OK'
        if cls.connect is not None:
            return cls.connect, err
        try:
            cls.connect = psycopg2.connect(
                dbname=MailConfig.dbname,
                user=MailConfig.dbuser,
                password=MailConfig.dbpassword,
                host=MailConfig.dbhost,
                port=MailConfig.dbport
                )
        except OperationalError as e:
            err = str(e)
        finally:
            return cls.connect, err

    # Disconnect the dify database
    @classmethod
    def disconnect_db(cls):
        if cls.connect is None: return
        cls.connect.close()
        cls.connect = None
        return cls.connect

    @classmethod
    def test_connect(cls,dbname,dbuser,dbpassword,dbhost,dbport):
            isconnect = False
            conn = None
            str = ""
            try:
                conn = psycopg2.connect(
                dbname=dbname,
                user=dbuser,
                password=dbpassword,
                host=dbhost,
                port=dbport
                )
                isconnect = True
            except OperationalError as e:
                isconnect = False
                str = str(e)
            finally:
                if conn is not None: conn.close()
                return isconnect, str


    # Query the email analysis logs from database
    @classmethod
    def query_logs_analysis(cls, dataset, selected_date):
        try:
            cursor = None
            cls.connect_db()
            cursor = cls.connect.cursor()
            cursor.execute(f"SELECT * FROM public.logs_analysis where DATE(analysis_date) = '{selected_date.Format("%Y-%m-%d")}';")
            rows = cursor.fetchall()
            dataset.ClearGrid()
            if dataset.GetNumberRows() < len(rows):
                dataset.AppendRows(len(rows) - dataset.GetNumberRows())
            idx = 0
            for row in rows:
                dataset.SetCellValue(idx, 0, str(row[0]))
                dataset.SetCellValue(idx, 1, row[1].strftime("%Y-%m-%d %H:%M:%S"))
                dataset.SetCellValue(idx, 2, row[2])
                dataset.SetCellValue(idx, 3, row[3])
                dataset.SetCellValue(idx, 4, row[4].strftime("%Y-%m-%d %H:%M:%S"))
                dataset.SetCellValue(idx, 5, row[5])
                dataset.SetCellValue(idx, 6, row[6])
                dataset.SetCellValue(idx, 7, row[7])
                idx=idx+1
                if idx % 2 == 1:
                    for col in range(dataset.GetNumberCols()):
                        dataset.SetCellBackgroundColour(idx, col, wx.Colour(222, 255, 255))
        except Exception as e:
            print("Error query_logs_analysis:", e)
        finally:
            if cursor is not None: cursor.close()

    # Insert the email analysis logs to database
    @classmethod
    def insert_logs_analysis(cls, llm_result, folder,mail_ReceivedTime, mail_sender, mail_subject, mail_body,level,factor_sentiment,factor_time):
        try:
            cursor = None
            cls.connect_db()
            cursor = cls.connect.cursor()
            insert_sql = """
                INSERT INTO public.logs_analysis (llm_result,folder,mail_ReceivedTime,mail_sender,mail_subject,mail_body,level,factor_sentiment,factor_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            data_to_insert=(llm_result,folder,mail_ReceivedTime,mail_sender,mail_subject,mail_body,level,factor_sentiment,factor_time)
            cursor.execute(insert_sql, data_to_insert)
            cls.connect.commit()
        except Exception as e:
            cls.connect.rollback()
            print("Error insert_logs_analysis:", e)
        finally:
            if cursor is not None: cursor.close()


    # Query the email auto reply logs from database
    @classmethod
    def query_logs_reply(cls, dataset, selected_date):
        try:
            cursor = None
            cls.connect_db()
            cursor = cls.connect.cursor()

            cursor.execute(f"SELECT * FROM public.logs_reply where DATE(reply_date) = '{selected_date}';")
            rows = cursor.fetchall()
            dataset.ClearGrid()
            if dataset.GetNumberRows() < len(rows):
                dataset.AppendRows(len(rows) - dataset.GetNumberRows())
            idx = 0
            for row in rows:
                #dataset.SetRowSize(idx, 25)
                dataset.SetCellValue(idx, 0, str(row[0]))
                dataset.SetCellValue(idx, 1, row[1].strftime("%Y-%m-%d %H:%M:%S"))
                dataset.SetCellValue(idx, 2, row[2])
                dataset.SetCellValue(idx, 3, row[3])
                dataset.SetCellValue(idx, 4, row[4].strftime("%Y-%m-%d %H:%M:%S"))
                dataset.SetCellValue(idx, 5, row[5])
                dataset.SetCellValue(idx, 6, row[6])
                dataset.SetCellValue(idx, 7, row[7])
                idx=idx+1
                if idx % 2 == 1:
                    for col in range(dataset.GetNumberCols()):
                        dataset.SetCellBackgroundColour(idx, col, wx.Colour(222, 255, 255))
        except Exception as e:
            print("Error query_logs_reply:", e)
        finally:
            if cursor is not None: cursor.close()

    # Insert the auto reply logs to database
    @classmethod
    def insert_logs_reply(cls,llm_result,reply_topic,mail_ReceivedTime,mail_sender,mail_subject,mail_body):
        try:
            cursor = None
            cls.connect_db()
            cursor = cls.connect.cursor()
            insert_sql = """
                INSERT INTO public.logs_reply (llm_result,reply_topic,mail_ReceivedTime,mail_sender,mail_subject,mail_body)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            data_to_insert=(llm_result,reply_topic,mail_ReceivedTime,mail_sender,mail_subject,mail_body)
            cursor.execute(insert_sql, data_to_insert)
            cls.connect.commit()
        except Exception as e:
            cls.connect.rollback()
            print("Error insert_logs_reply:", e)
        finally:
            if cursor is not None: cursor.close()

    # Query Sentiment Factor data from database
    @classmethod
    def query_sentiment_factor(cls, dataset):
        try:
            cursor = None
            cls.connect_db()
            cursor = cls.connect.cursor()

            cursor.execute(f"SELECT * FROM public.sentiment_factor;")
            rows = cursor.fetchall()
            dataset.ClearGrid()
            if dataset.GetNumberRows() < len(rows):
                dataset.AppendRows(len(rows) - dataset.GetNumberRows())
            idx = 0
            for row in rows:
                #dataset.SetRowSize(idx, 25)
                cls.array_sentiment.append(row[1])
                cls.array_sentiment_factor.append(row[2])
                dataset.SetCellValue(idx, 0, str(row[0]))
                dataset.SetCellValue(idx, 1, row[1])
                dataset.SetCellValue(idx, 2, row[2])
                idx=idx+1
                if idx % 2 == 1:
                    for col in range(dataset.GetNumberCols()):
                        dataset.SetCellBackgroundColour(idx, col, wx.Colour(222, 255, 255))
        except Exception as e:
            print("Error query_sentiment_factor:", e)
        finally:
            if cursor is not None: cursor.close()

    # Update Sentiment Factor data from database
    @classmethod
    def update_sentiment_factor(cls, dataset):
        try:
            cursor = None
            cls.connect_db()
            cursor = cls.connect.cursor()
            n=0
            for row in range(dataset.GetNumberRows()):
                update_sql = f"update public.sentiment_factor set factor = '{dataset.GetCellValue(row, 2)}' where id = {dataset.GetCellValue(row, 0)} ;"
                #print(f"update_sql={update_sql}")
                cursor.execute(update_sql)
                n = n+1
            cls.connect.commit()
        except Exception as e:
            cls.connect.rollback()
            print("Error update_sentiment_factor:", e)
            n=-1
        finally:
            if cursor is not None: cursor.close()
            return n

    # Query Sentiment Factor data from database
    @classmethod
    def query_time_factor(cls, dataset):
        try:
            cursor = None
            cls.connect_db()
            cursor = cls.connect.cursor()

            cursor.execute(f"SELECT * FROM public.time_factor;")
            rows = cursor.fetchall()
            dataset.ClearGrid()
            if dataset.GetNumberRows() < len(rows):
                dataset.AppendRows(len(rows) - dataset.GetNumberRows())
            idx = 0
            for row in rows:
                cls.array_time.append(row[1])
                cls.array_time_factor.append(row[2])
                #dataset.SetRowSize(idx, 25)
                dataset.SetCellValue(idx, 0, str(row[0]))
                dataset.SetCellValue(idx, 1, row[1])
                dataset.SetCellValue(idx, 2, row[2])
                idx=idx+1
                if idx % 2 == 1:
                    for col in range(dataset.GetNumberCols()):
                        dataset.SetCellBackgroundColour(idx, col, wx.Colour(222, 255, 255))
        except Exception as e:
            print("Error query_time_factor:", e)
        finally:
            if cursor is not None: cursor.close()
            return len(rows)

    # Update Time Factor data from database
    @classmethod
    def update_time_factor(cls, dataset):
        try:
            cursor = None
            cls.connect_db()
            cursor = cls.connect.cursor()
            n = 0
            for row in range(dataset.GetNumberRows()):
                update_sql = f"update public.time_factor set factor = '{dataset.GetCellValue(row, 2)}' where id = {dataset.GetCellValue(row, 0)};"
                cursor.execute(update_sql)
                n = n +1
            cls.connect.commit()
        except Exception as e:
            cls.connect.rollback()
            print("Error update_time_factor:", e)
            n = -1
        finally:
            if cursor is not None: cursor.close()
            return n