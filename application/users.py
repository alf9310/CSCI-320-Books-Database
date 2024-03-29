from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from datetime import datetime
from typing import Union
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class Users(Base):
    '''
    Defines Users
    '''
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True) 
    username = Column(String)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    created_date = Column(DateTime, default=datetime.now)
    last_accessed = Column(DateTime, default=datetime.now)

    logs = relationship("Log", back_populates="user")
    
    '''
    User Constructor
    '''
    def __init__(self, uid, username, password, first_name, last_name, email):
        self.uid = uid
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    '''
    To-string for Users
    '''
    def __str__(self):
        return (f"Users(uid={self.uid}, username='{self.username}', password='{self.password}', "
        f"first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}', "
        f"created_date='{self.created_date}', last_accessed='{self.last_accessed}'")
    
    '''
    Creates a new User and add them to the database
    '''
    @classmethod
    def create(cls, session, username, password, first_name, last_name, email):
        try:
            max_uid = session.query(func.max(cls.uid)).scalar() or 0  # Get the maximum uid, or default to 0 if table is empty
            new_user = cls(uid = max_uid + 1, username=username, password=password, first_name=first_name, last_name=last_name, email=email)
            session.add(new_user)
            session.commit()
            return new_user
        except Exception as e:
            print(e)
            session.rollback()
            return None
        
    '''
    Constructs an SQLAlchemy query based on the search parameters provided. 
    It filters the query by uid, first_name, last_name, and username.
    Order by order_by and can limit the number of results returned with limit.
    '''
    @classmethod
    def search(cls, session, uid=None, first_name=None, last_name=None, username=None, password=None, email=None, order_by=None, limit=None):
        query = session.query(Users)

        if uid:
            query = query.filter(Users.uid == uid)
        if first_name:
            query = query.filter(Users.first_name.ilike(f"%{first_name}%"))
        if last_name:
            query = query.filter(Users.last_name.ilike(f"%{last_name}%"))
        if username:
            query = query.filter(Users.username.ilike(f"%{username}%"))
        if password:
            query = query.filter(Users.password.ilike(f"%{password}%"))
        if email:
            query = query.filter(Users.email.ilike(f"%{email}%"))

        total_count = query.count()

        if order_by:
            if hasattr(Users, order_by):
                query = query.order_by(getattr(Users, order_by))
        if limit:
            query = query.limit(limit)

        return query, total_count
    
    '''
    Update Users & last_accessed
    '''
    def save(self, session):
        self.last_accessed = datetime.now()
        session.commit()

    '''
    Delete Users
    '''
    def delete(self, session):
        session.delete(self)
        session.commit()