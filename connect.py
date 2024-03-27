import os
import psycopg2
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

from users import Users

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

        '''
        # Check user columns in database
        metadata = MetaData()
        metadata.reflect(bind=engine) 
        print(metadata.tables.keys())  # Print table names
        print(metadata.tables['users'].columns)  # Print table structure for 'users' table
        '''

        # ----------------Testing User usage----------------
        users = session.query(Users).all()
        for user in users:
            print(user)
        print()

        # Create a user
        new_user = Users.create(session, first_name = "John", last_name = "Doe", username = "123JohnnyBoy", password = "password123")

        # Query users with the first name John
        results, total_count = Users.search(session, first_name="John")
        print(total_count, "Users with the first name John")
        for result in results:
            print(result)
        print()

        # Query users with the last name Smith
        results, total_count = Users.search(session, last_name="Smith")
        print(total_count, "Users with the last name Smith")
        for result in results:
            print(result)
        print()

        # Update a user
        new_user.last_name = "Smith"
        new_user.save(session)

        # Query users with the last name Smith
        results, total_count = Users.search(session, last_name="Smith")
        print(total_count, "Users with the last name Smith")
        for result in results:
            print(result)
        print()

        # Delete a user
        new_user.delete(session)

        # Query users with the last name Smith
        results, total_count = Users.search(session, last_name="Smith")
        print(total_count, "Users with the last name Smith")
        for result in results:
            print(result)
        print()

        session.close()

except:
    print("Connection failed")
