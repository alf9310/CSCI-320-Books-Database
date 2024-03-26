from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from datetime import datetime
from typing import Union

Base = declarative_base()

class User(Base):
    '''
    Defines Users
    '''
    __tablename__ = 'users'
    username = Column(String)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    created_date = Column(DateTime, default=datetime.now)
    last_accessed = Column(DateTime, default=datetime.now)
    uid = Column(Integer, primary_key=True) #TODO make sure this is generating unique instances

    def __init__(self, uid = None, created_date = None, last_accessed = None, first_name = None, last_name = None, username = None, password = None):
        self.uid = uid
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.created_date = created_date
        self.last_accessed = last_accessed
    
    @property
    def uid(self):
        return self.user.uid

    '''
    Creates a new User and adds it to the database
    '''
    @classmethod
    def create(cls, session, uid: int, first_name: str, last_name: str, username: str, password: str) -> Union["User", None]:
        try:
            new_user = User(session, uid = uid, created_date=datetime.now(), last_accessed=datetime.now(), first_name=first_name, last_name=last_name, username=username, password=password)
            session.add(new_user)
            session.commit()
            return new_user
        except Exception as e:
            print(e)
            session.rollback()
            return None

    '''
    Update Users & last accessed
    '''
    def save(self):
        self.user.last_accessed = datetime.now()
        self.session.commit()

    '''
    Delete Users
    '''
    def delete(self):
        self.session.delete(self.user)
        self.session.commit()

    '''
    Creates a new User instance from the session and user
    '''
    @classmethod
    def _from_search(cls, session, user):
        return User(session, user)

    '''
    Constructs an SQLAlchemy query based on the search parameters provided. 
    It filters the query by uid, first_name, last_name, and username.
    '''
    @classmethod
    def search(cls, session, pagination, uid=None, first_name=None, last_name=None, username=None):
        query = session.query(User)

        if uid:
            query = query.filter(User.uid == uid)
        if first_name:
            query = query.filter(User.first_name.ilike(f"%{first_name}%"))
        if last_name:
            query = query.filter(User.last_name.ilike(f"%{last_name}%"))
        if username:
            query = query.filter(User.username.ilike(f"%{username}%"))

        total_count = query.count()

        if pagination:
            if 'order' in pagination:
                query = query.order_by(*pagination['order'])
            if 'offset' in pagination:
                query = query.offset(pagination['offset'])
            if 'limit' in pagination:
                query = query.limit(pagination['limit'])

        results = query.all()
        return results, total_count
    