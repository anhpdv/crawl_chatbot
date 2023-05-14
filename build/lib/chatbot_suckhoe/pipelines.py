import mysql.connector
from mysql.connector import errorcode
import json
import psycopg2
class MySQLPipeline:
    config = {
        'host': "103.252.1.139",
        'database': "Chatbot",
        'user': "postgre_soda",
        'port': 5422,
        'password': "CIST#soda123"}

    def __init__(self):
        self.dateLimit = 20  # Number of days to check
        self.tolerables = 0
        self.maxTolerables = 30
        self.last = None
        self.cnx = psycopg2.connect(
            host="103.252.1.139",
            database="Chatbot",
            user="postgre_soda",
            port=5422,
            password="CIST#soda123")

    def process_item(self, item, spider):
        print("Connect DB Postgre")
        cursor = self.cnx.cursor()

        if spider.name == "vinmec_benh":
            check_query = "SELECT count(*) FROM \"benh\" WHERE link = '" + item["link"] + "'"
            cursor.execute(check_query)
            myresult = cursor.fetchall()
            for x in myresult:
                exist = x[0]
            if exist == 0:
                try:
                    cursor.execute("INSERT INTO \"benh\" (ten_benh, nguyen_nhan, trieu_chung, bien_phap_chan_doan, bien_phap_dieu_tri, phong_ngua, link) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                        item["ten_benh"], item["nguyen_nhan"], item["trieu_chung"], item["bien_phap_chan_doan"], item["bien_phap_dieu_tri"], item["phong_ngua"], item["link"]))
                    self.cnx.commit()
                except Exception as e:
                    print(e)
                    self.cnx.rollback()

                print("Da them xong bảng bệnh")
        else:
            check_query = "SELECT count(*) FROM \"data_qna2\" WHERE url = '" + item["link"] + "'"
            cursor.execute(check_query)
            myresult = cursor.fetchall()
            for x in myresult:
                exist = x[0]
            if exist == 0:
                try:
                    cursor.execute("INSERT INTO \"data_qna2\" (question, answer, url) VALUES ('{}', '{}', '{}')".format(item["question"], item["answer"], item["link"]))
                    self.cnx.commit()
                except Exception as e:
                    print(e)
                    self.cnx.rollback()
                print("Da them xong")

