import os
import psycopg2
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DB_NAME = "p320_30"

try:
    with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                            ssh_username=USERNAME,
                            ssh_password=PASSWORD,
                            remote_bind_address=('127.0.0.1', 5432)) as server:
        server.start()
        print("SSH tunnel established")
        params = {
            'database': DB_NAME,
            'user': USERNAME,
            'password': PASSWORD,
            'host': 'localhost',
            'port': server.local_bind_port
        }


        conn = psycopg2.connect(**params)
        curs = conn.cursor()
        print("Database connection established")

        # # database work

        # postgreSQL_select_Query = "select * from ryan_ong_table"

        # curs.execute(postgreSQL_select_Query)
        # print("Selecting rows from mobile table using curs.fetchall")
        # mobile_records = curs.fetchall()

        # print("Print each row and it's columns values")
        # for row in mobile_records:
        #     print("test = ", row[0])
        # conn.close()
except:
    print("Connection failed")
