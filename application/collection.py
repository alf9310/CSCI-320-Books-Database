from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from datetime import datetime
from typing import Union
from sqlalchemy.sql.expression import func

Base = declarative_base()

class Collection(Base):
    '''
    Defines Collection
    '''
    __tablename__ = 'collection'
    cid = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("users.uid"))
    name = Column(String)
    created_date = Column(DateTime, default=datetime.now)

    '''
    Collection Constructor
    '''
    def __init__(self, cid, uid, name):
        self.cid = cid
        self.uid = uid
        self.name = name

    '''
    To-string for Collection
    '''
    def __str__(self):
        return (f"Collection(cid={self.cid}, uid={self.uid}, name='{self.name}',"
                f" created_date='{self.created_date}'")
    
    '''
    Creates a new Collection and adds it to the database
    '''
    @classmethod
    def create(cls, session, name, uid):
        try:
            max_cid = session.query(func.max(cls.cid)).scalar() or 0  # Get the maximum uid, or default to 0 if table is empty
            new_collection = cls(cid = max_cid + 1, name=name, uid=uid)
            session.add(new_collection)
            session.commit()
            return new_collection
        except Exception as e:
            print(e)
            session.rollback()
            return None
        
    '''
    Constructs an SQLAlchemy query based on the search parameters provided. 
    A UID must be provided, as this query will be used to view the
    collections of a specific user.
    It can filter by collection name.
    Order by order_by and can limit the number of results returned with limit.
    '''
    @classmethod
    def search(cls, session, uid=None, name=None, order_by=None, limit=None):
        query = session.query(Collection)

        if uid:
            query = query.filter(Collection.uid == uid)
        if name:
            query = query.filter(Collection.name.ilike(f"%{name}%"))

        total_count = query.count()

        if order_by:
            if hasattr(Collection, order_by):
                query = query.order_by(getattr(Collection, order_by))
        if limit:
            query = query.limit(limit)

        return query, total_count
            
    '''
    Update the Collection
    '''
    def save(self, session):
        session.commit()

    '''
    Delete a Collection
    '''
    def delete(self, session):
        session.delete(self)
        session.commit()

class In_Collection(Base):
    '''
    Defines In_Collection
    '''
    __tablename__ = 'in_collection'
    cid = Column(Integer, ForeignKey("collection.cid"), primary_key=True)
    bid = Column(Integer, ForeignKey("book.bid"), primary_key=True)
    date_added = Column(DateTime, default=datetime.now)

    '''
    In_Collection Constructor
    '''
    def __init__(self, cid, bid):
        self.cid = cid
        self.bid = bid

    '''
    To-string for In_Collection
    '''
    def __str__(self):
        return (f"In_Collection(cid={self.cid}, bid={self.bid},"
                f" date_added='{self.date_added}'")
    
    '''
    Creates a new In_Collection and adds it to the database
    '''
    @classmethod
    def create(cls, session, cid, bid):
        try:
            new_in_collection = cls(cid=cid, bid=bid)
            session.add(new_in_collection)
            session.commit()
            return new_in_collection
        except Exception as e:
            print(e)
            session.rollback()
            return None
        
    '''
    Constructs an SQLAlchemy query based on the search parameters provided. 
    A CID must be provided, as this query will be used to view the
    books in a specific collection.
    Order by order_by and can limit the number of results returned with limit.
    '''
    @classmethod
    def search(cls, session, cid=None, order_by=None, limit=None):
        query = session.query(In_Collection)

        if cid:
            query = query.filter(In_Collection.cid == cid)

        total_count = query.count()

        if order_by:
            if hasattr(In_Collection, order_by):
                query = query.order_by(getattr(In_Collection, order_by))
        if limit:
            query = query.limit(limit)

        return query, total_count
    
    '''
    Update the In_Collection
    '''
    def save(self, session):
        session.commit()

    '''
    Delete an In_Collection (remove from collection)
    '''
    def delete(self, session):
        session.delete(self)
        session.commit()