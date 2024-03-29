from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import ForeignKey
from datetime import datetime
from typing import Union
from sqlalchemy.sql.expression import func
from book import Book
from users import Users

Base = declarative_base()

class Rates(Base):
    '''Defines Rates'''

    __tablename__ = 'rates'
    uid = Column(Integer, ForeignKey(Users.uid), primary_key = True)
    bid = Column(Integer, ForeignKey(Book.bid), primary_key = True)
    rating = Column(Integer)

    def __init__(self, uid, bid, rating):
        self.uid = uid
        self.bid = bid
        self.rating = rating
    
    def __str__(self):
        return(f"Rates(uid={self.uid}, bid={self.bid}, rating={self.rating})")
    
    '''
    Creates a new Rates and adds it to the database
    '''
    @classmethod
    def create(cls, session, uid, bid, rating_received):
        try:
            new_rating = cls(uid=uid, bid=bid, rating = max(min(rating_received, 5), 1))
            session.add(new_rating)
            session.commit()
            return new_rating
        except Exception as e:
            print(e)
            session.rollback()
            return None
    
    def change_rating(session, uid, bid, new_rating):
        results, count = Rates.search(session, uid, bid)
        if(count != 1):
            print("Doesn't exist")
            return False
        else:
            rating_to_change = results.first()
            rating_to_change.rating = max(min(new_rating, 5), 1)
            session.commit()
            return True

    
    
    @classmethod
    def search(cls, session, uid=None, bid=None, rating=None, order_by=None):
        query = session.query(Rates)
        if uid:
            query = query.filter(Rates.uid == uid)
        if bid:
            query = query.filter(Rates.bid == bid)
        if rating:
            query = query.filter(Rates.rating == rating)

        total_count = query.count()

        if order_by:
            if hasattr(Rates, order_by):
                query = query.order_by(getattr(Rates, order_by))

        return query, total_count

    def save(self, session):
        session.commit()
    

    def rating_view(session, uid):
        query = session.query(Rates)
        query = query.filter(Rates.uid == uid)

        count = query.count()
        if count == 0:
            print("You have not rated any books")
        else:
            for entry in query:
                title = (session.query(Book).filter_by(bid=entry.bid).first()).title
                print(f"\tTitle: {title}, Rating: {entry.rating}")