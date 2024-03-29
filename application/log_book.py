from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy.sql.expression import func
from sqlalchemy import text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Log(Base):
    '''
    Defines Log
    '''
    __tablename__ = 'logs'
    bid = Column(Integer, ForeignKey('book.bid'), primary_key=True)
    uid = Column(Integer, ForeignKey('users.bid'), primary_key=True)
    
    start_time = Column(DateTime, primary_key=True) 
    end_time = Column(DateTime)
    
    start_page = Column(Integer)
    end_page = Column(Integer)


    '''
    Log Constructor
    '''
    def __init__(self, bid, uid, start_time, end_time, start_page, end_page):
        self.bid = bid
        self.uid = uid
        self.start_time = start_time
        self.end_time = end_time
        self.start_page = start_page
        self.end_page = end_page

    '''
    To-string for Log
    '''
    def __str__(self):
        return(f"Log(bid={self.bid}, uid={self.uid}, start_time={self.start_time}, \
                    end_time={self.end_time}, start_page={self.start_page}, end_page={self.end_page})")

    '''
    Creates a new log and adds it to the DB
    '''
    @classmethod
    def create(cls, session, bid, uid, start_time, end_time, start_page, end_page):
        try:
            new_log = cls(bid, uid, start_time, end_time, start_page, end_page)
            session.add(new_log)
            session.commit()
            return new_log()
        except Exception as e:
            print(e)
            session.rollback()
            return None

    '''
    Constructs an SQLAlchemy query based on the search parameters provided. 
    A UID must be provided, as this query will be used to view the
    collections of a specific user.
    It can filter by log name.
    Order by order_by and can limit the number of results returned with limit.
    '''
    @classmethod
    def search(cls, session, bid=None, uid=None, start_time=None, end_time=None, start_page=None, end_page=None, order_by=None, limit=None):
        if bid:
            query = query.filter(Log.bid == bid)
        if uid:
            query = query.filter(Log.uid == uid)
        if start_time:
            query = query.filter(Log.start_time >= start_time)
        if end_time:
            query = query.filter(Log.end_time <= end_time)
        if start_page:
            query = query.filter(Log.start_page == start_page)
        if end_page:
            query = query.filter(Log.end_page == end_page)

        total_count = query.count()

        if order_by:
            if hasattr(Log, order_by):
                query = query.order_by(getattr(Log, order_by))
        if limit:
            query = query.limit(limit)

        return query, total_count
    
    '''
    Update Log
    '''
    def save(self, session):
        session.commit()

    '''
    Delete Book
    '''
    def delete(self, session):
        session.delete(self)
        session.commit()

    # # Define relationships
    # book = relationship("Book", back_populates="logs")
    # user = relationship("User", back_populates="logs")
