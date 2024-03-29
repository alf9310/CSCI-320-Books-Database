from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy.sql.expression import func
from sqlalchemy import text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from users import Base as UserBase
from book import Book

class Log(UserBase):
    '''
    Defines Log
    '''
    __tablename__ = 'logs'
    bid = Column(Integer, ForeignKey(UserBase.metadata.tables['book'].c.bid), primary_key=True)
    uid = Column(Integer, ForeignKey(UserBase.metadata.tables['users'].c.uid), primary_key=True)
    
    start_time = Column(DateTime, primary_key=True) 
    end_time = Column(DateTime)
    
    start_page = Column(Integer)
    end_page = Column(Integer)

    # Define relationships
    book = relationship("Book", back_populates="logs")
    user = relationship("Users", back_populates="logs")


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
            new_log = cls(bid=bid, uid=uid, start_time=start_time, end_time=end_time, start_page=start_page, end_page=end_page)
            session.add(new_log)
            session.commit()
            print("Log created successfully")
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
    def search(cls, session, query=None, bid=None, uid=None, start_time=None, end_time=None, start_page=None, end_page=None, order_by=None, limit=None):
        if query is None:
            query = session.query(Log)
        
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
    Delete Log
    '''
    def delete(self, session):
        session.delete(self)
        session.commit()

    '''
    Get a list of all logs of some user
    '''
    def listLogs(session, uid):
        query = session.query(Log)
        query = query.filter(Log.uid == uid)

        count = query.count()
        if count == 0:
            print("You have no logs!")
        else:
            # entry is a log object
            for log in query:
                book, total_count = Book.search(session, bid=log.bid)
                print(book[0].title)
                print(f"\tStart page: {log.start_page}, End page: {log.end_page}")
                print(f"\tStart time: {log.start_time}, End Time: {log.end_time}")
