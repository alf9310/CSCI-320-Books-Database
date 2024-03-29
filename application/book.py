from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy.sql.expression import func
from sqlalchemy import text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import and_


Base = declarative_base()

class Book(Base):
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
    def __str__(self):
        #TODO must print ratings 
        authors = ", ".join([written.person.person_name for written in self.written_by])
        publishers = ", ".join([published.person.person_name for published in self.published_by])
        return (f"Title: '{self.title}', Authors: '{authors}', Publishers: '{publishers}', Length: '{self.length}', Audience: ages {self.min_age}-{self.max_age}")
    
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
    def search(cls, session, query=None, bid=None, title=None, release_date=None, author=None, publisher=None, genre=None, order_by=None, limit=None):
        # TODO order by nama alphabetically by default
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

        total_count = query.count()

        if order_by:
            if hasattr(Book, order_by):
                query = query.order_by(getattr(Book, order_by))
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

class WrittenBy(Base):
    '''
    Defines relationship between Book and Person for writing
    '''
    __tablename__ = 'written_by'
    bid = Column(Integer, ForeignKey('book.bid'), primary_key=True)
    pid = Column(Integer, ForeignKey('person.pid'), primary_key=True)

    # Define relationships
    book = relationship("Book", back_populates="written_by")
    person = relationship("Person", back_populates="written_by")

class PublishedBy(Base):
    '''
    Defines relationship between Book and Person for publishing
    '''
    __tablename__ = 'published_by'
    bid = Column(Integer, ForeignKey('book.bid'), primary_key=True)
    pid = Column(Integer, ForeignKey('person.pid'), primary_key=True)

    # Define relationships
    book = relationship("Book", back_populates="published_by")
    person = relationship("Person", back_populates="published_by")

class EditedBy(Base):
    '''
    Defines relationship between Book and Person for editing
    '''
    __tablename__ = 'edited_by'
    bid = Column(Integer, ForeignKey('book.bid'), primary_key=True)
    pid = Column(Integer, ForeignKey('person.pid'), primary_key=True)

    # Define relationships
    book = relationship("Book", back_populates="edited_by")
    person = relationship("Person", back_populates="edited_by")

class Person(Base):
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

class HasGenre(Base):
    '''
    Defines relationship between Genre and Book
    '''
    __tablename__ = 'has_genre'
    bid = Column(Integer, ForeignKey('book.bid'), primary_key=True)
    gid = Column(Integer, ForeignKey('genre.gid'), primary_key=True)

    # Define relationships
    book = relationship("Book", back_populates="has_genre")
    genre = relationship("Genre", back_populates="has_genre")

class Genre(Base):
    '''
    Defines Genre
    '''
    __tablename__ = 'genre'
    gid = Column(Integer, primary_key=True)
    genre_name = Column(String)

    # Define relationships
    has_genre = relationship("HasGenre", back_populates="genre")

class ReleasedAs(Base):
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

class Format(Base):
    '''
    Defines Format
    '''
    __tablename__ = 'format'
    fid = Column(Integer, primary_key=True)
    format_name = Column(String)

    # Define relationships
    released_books = relationship("ReleasedAs", back_populates="format")