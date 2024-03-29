from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.expression import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy.sql import text
from users import Base as UserBase, Users

class Book(UserBase):
    '''
    Defines Book
    '''
    __tablename__ = 'book'
    bid = Column(Integer, primary_key=True) 
    length = Column(Integer)
    title = Column(String)
    min_age = Column(String)
    max_age = Column(String)

    # Define relationships
    written_by = relationship("WrittenBy", back_populates="book")
    published_by = relationship("PublishedBy", back_populates="book")
    edited_by = relationship("EditedBy", back_populates="book")
    has_genre = relationship("HasGenre", back_populates="book")
    released_formats = relationship("ReleasedAs", back_populates="book")
    logs = relationship("Log", back_populates="book")

    '''
    Book Constructor
    '''
    def __init__(self, bid, length, title, min_age, max_age):
        self.bid = bid
        self.length = length
        self.title = title
        self.min_age = min_age
        self.max_age = max_age

    '''
    To-string for Books
    '''
    def __str__(self, session=None):
        if session is not None:
            authors = ", ".join([written.person.person_name for written in self.written_by if written.person is not None])        
            publishers = ", ".join([published.person.person_name for published in self.published_by if published.person is not None])
            rating = Rates.get_average_rating(session, self.bid)
            return (f"Title: '{self.title}', Authors: '{authors}', Publishers: '{publishers}', Length: '{self.length}', Audience: Ages {self.min_age}-{self.max_age}, Rating: {rating}")
        else:
            authors = ", ".join([written.person.person_name for written in self.written_by if written.person is not None])        
            publishers = ", ".join([published.person.person_name for published in self.published_by if published.person is not None])
            return (f"Title: '{self.title}', Authors: '{authors}', Publishers: '{publishers}', Length: '{self.length}', Audience: Ages {self.min_age}-{self.max_age}")


    '''
    Creates a new Book and add it to the database
    '''
    @classmethod
    def create(cls, session, length, title, min_age, max_age):
        try:
            max_bid = session.query(func.max(cls.bid)).scalar() or 0  # Get the maximum bid, or default to 0 if table is empty
            new_book = cls(uid = max_bid + 1, length=length, title=title, min_age=min_age, max_age=max_age)
            session.add(new_book)
            session.commit()
            return new_book
        except Exception as e:
            print(e)
            session.rollback()
            return None
        
    '''
    Constructs an SQLAlchemy query based on the search parameters provided. 
    It filters the query by bid, title, release date, authors, publisher, or genre
    Order by order_by and can limit the number of results returned with limit.
    '''
    @classmethod
    def search(cls, session, query=None, bid=None, title=None, release_date=None, author=None, publisher=None, genre=None, order_by=None, descending = False, limit=None):
        if query is None:
            query = session.query(Book)

        if bid:
            query = query.filter(Book.bid == bid)
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if release_date:
            min_release_date, max_release_date = release_date
            # Join with ReleasedAs table to access the release date
            query = query.join(ReleasedAs).filter(and_(ReleasedAs.date >= min_release_date, ReleasedAs.date <= max_release_date))
        if author:
            # Join the WrittenBy and Person tables to filter by author
            query = query.join(WrittenBy).join(Person).filter(Person.person_name.ilike(f"%{author}%"))
        if publisher:
            # Join the PublishedBy and Person tables to filter by publisher
            query = query.join(PublishedBy).join(Person).filter(Person.person_name.ilike(f"%{publisher}%"))
        if genre:
            # Join the HasGenre and Genre tables to filter by genre
            query = query.join(HasGenre).join(Genre).filter(Genre.genre_name.ilike(f"%{genre}%"))

        if order_by and order_by in ["title", "publisher", "genre", "release_year"]:
            # Determine the column to order by
            column = getattr(cls, order_by)
            print("Sorting by:", order_by)
            print("Descending order:", descending)
            if descending:
                print("Applying descending order")
                query = query.order_by(column.desc())
            else:
                print("Applying ascending order")
                query = query.order_by(column)


        total_count = query.count()


        if limit:
            query = query.limit(limit)

        return query, total_count
    
    '''
    Update Book
    '''
    def save(self, session):
        session.commit()

    '''
    Delete Book
    '''
    def delete(self, session):
        session.delete(self)
        session.commit()

class WrittenBy(UserBase):
    '''
    Defines relationship between Book and Person for writing
    '''
    __tablename__ = 'written_by'
    bid = Column(Integer, ForeignKey('book.bid'), primary_key=True)
    pid = Column(Integer, ForeignKey('person.pid'), primary_key=True)

    # Define relationships
    book = relationship("Book", back_populates="written_by")
    person = relationship("Person", back_populates="written_by")

class PublishedBy(UserBase):
    '''
    Defines relationship between Book and Person for publishing
    '''
    __tablename__ = 'published_by'
    bid = Column(Integer, ForeignKey('book.bid'), primary_key=True)
    pid = Column(Integer, ForeignKey('person.pid'), primary_key=True)

    # Define relationships
    book = relationship("Book", back_populates="published_by")
    person = relationship("Person", back_populates="published_by")

class EditedBy(UserBase):
    '''
    Defines relationship between Book and Person for editing
    '''
    __tablename__ = 'edited_by'
    bid = Column(Integer, ForeignKey('book.bid'), primary_key=True)
    pid = Column(Integer, ForeignKey('person.pid'), primary_key=True)

    # Define relationships
    book = relationship("Book", back_populates="edited_by")
    person = relationship("Person", back_populates="edited_by")

class Person(UserBase):
    '''
    Defines Person
    '''
    __tablename__ = 'person'
    pid = Column(Integer, primary_key=True)
    person_name = Column(String)

    # Define relationships
    written_by = relationship("WrittenBy", back_populates="person")
    published_by = relationship("PublishedBy", back_populates="person")
    edited_by = relationship("EditedBy", back_populates="person")

class HasGenre(UserBase):
    '''
    Defines relationship between Genre and Book
    '''
    __tablename__ = 'has_genre'
    bid = Column(Integer, ForeignKey('book.bid'), primary_key=True)
    gid = Column(Integer, ForeignKey('genre.gid'), primary_key=True)

    # Define relationships
    book = relationship("Book", back_populates="has_genre")
    genre = relationship("Genre", back_populates="has_genre")

class Genre(UserBase):
    '''
    Defines Genre
    '''
    __tablename__ = 'genre'
    gid = Column(Integer, primary_key=True)
    genre_name = Column(String)

    # Define relationships
    has_genre = relationship("HasGenre", back_populates="genre")

class ReleasedAs(UserBase):
    '''
    Defines relationship between Book and Format
    '''
    __tablename__ = 'released_as'
    bid = Column(Integer, ForeignKey('book.bid'), primary_key=True)
    fid = Column(Integer, ForeignKey('format.fid'), primary_key=True)
    date = Column(DateTime)

    # Define relationships
    book = relationship("Book", back_populates="released_formats")
    format = relationship("Format", back_populates="released_books")

class Format(UserBase):
    '''
    Defines Format
    '''
    __tablename__ = 'format'
    fid = Column(Integer, primary_key=True)
    format_name = Column(String)

    # Define relationships
    released_books = relationship("ReleasedAs", back_populates="format")

class Rates(UserBase):
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
    

    def get_average_rating(session, bid):
        query = session.query(Rates)
        query = query.filter(Rates.bid == bid)

        count = query.count()
        if count == 0:
            return "-"
        else:
            rating_count = 0
            average_rating = 0
            for entry in query:
                average_rating += entry.rating
                rating_count += 1
            average_rating /= rating_count
            return str(average_rating)


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