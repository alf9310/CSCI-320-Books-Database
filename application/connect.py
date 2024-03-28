import os
import psycopg2
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DB_NAME = "p320_30"

def create_ssh_tunnel():
    try:
        server = SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                     ssh_username=USERNAME,
                                     ssh_password=PASSWORD,
                                     remote_bind_address=('127.0.0.1', 5432))
        server.start()
        print("SSH tunnel established")
        return server
    except Exception as e:
        print("Failed to establish SSH tunnel:", e)
        return None

def create_database_session(server):
    try:
        params = {
            'database': DB_NAME,
            'user': USERNAME,
            'password': PASSWORD,
            'host': 'localhost',
            'port': server.local_bind_port
        }
        conn = psycopg2.connect(**params)
        curs = conn.cursor()

        # Build SQLAlchemy database URL with SSH tunnel
        db_url = f'postgresql://{USERNAME}:{PASSWORD}@127.0.0.1:{server.local_bind_port}/{DB_NAME}'

        # Create SQLAlchemy engine and session
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        session = Session()

        print("Database connection established")
        return session
    except Exception as e:
        print("Failed to establish database connection:", e)
        return None

def test_connection():
    server = create_ssh_tunnel()
    if server:
        session = create_database_session(server)
        return session
    return None

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

        return record

