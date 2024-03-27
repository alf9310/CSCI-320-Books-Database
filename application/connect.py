import os
import psycopg2
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DB_NAME = "p320_30"

def test_connection() -> None:
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
            print("Database connection established")
    except:
        print("Connection failed")


def execute_query(query: str) -> list:
    with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                            ssh_username=USERNAME,
                            ssh_password=PASSWORD,
                            remote_bind_address=('127.0.0.1', 5432)) as server:
        server.start()
        params = {
            'database': DB_NAME,
            'user': USERNAME,
            'password': PASSWORD,
            'host': 'localhost',
            'port': server.local_bind_port
        }

        conn = psycopg2.connect(**params)
        curs = conn.cursor()
        
        # database work
        postgreSQL_select_Query = query

        curs.execute(postgreSQL_select_Query)
        record = curs.fetchall()

        return record;
    # errors not caught