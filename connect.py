import os
import psycopg2
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

#from user import User

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
            'host': '127.0.0.1',
            'port': server.local_bind_port
        }

        conn = psycopg2.connect(**params)
        curs = conn.cursor()
        print("Database connection established")

        # Build SQLAlchemy database URL with SSH tunnel
        db_url = f'postgresql://{USERNAME}:{PASSWORD}@127.0.0.1:{server.local_bind_port}/{DB_NAME}'

        # Create SQLAlchemy engine and session
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Check user columns
        metadata = MetaData()
        metadata.reflect(bind=engine) 
        print(metadata.tables.keys())  # Print table names
        print(metadata.tables['users'].columns)  # Print table structure for 'users' table

        '''
        # Use the session to interact with the database using SQLAlchemy
        # ----------------Testing User usage----------------

        # Create a user
        new_user = User.create(session, 1000000, "John", "Doe", "JohnnyBoy", "password123")

        # Query users
        # Call the search method with the provided session and first_name parameter
        results, total_count = User.search(session, {}, first_name="John")

        # Print the results
        for user in results:
            print(user.first_name, user.last_name)

        # Update a user
        new_user.last_name = "Smith"
        new_user.save()

        # Delete a user
        new_user.delete()

        # Call the search method with the provided session and first_name parameter
        results, total_count = User.search(session, {}, first_name="John")

        # Print the results
        for user in results:
            print(user.first_name, user.last_name)
        '''

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
