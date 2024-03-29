from math import ceil
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
            max_cid = session.query(func.max(cls.cid)).scalar() or 0  # Get the maximum cid, or default to 0 if table is empty
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
    def search(cls, session, cid=None, uid=None, name=None, order_by=None, limit=None):
        query = session.query(Collection)

        if cid:
            query = query.filter(Collection.cid == cid)
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

'''
Function for creating a new collection.
Prompts the user for the name of the collection.
@param session - object for the current session
@param uid - the ID of the currently logged in user
@return True if need to refresh, False if not
'''
def create_collection(session, uid):
    new_collection
    
    while (True):
        new_name = input("Please enter the collection name. [q to quit]")
        if (new_name == ""):
            print("Please enter a name.")
            continue
        if (len(new_name) > 50):
            print("This name is too long!")
            continue
        if (new_name == "q"):
            return False
        new_collection = Collection.create(session, name=new_name, uid=uid)
        
        new_collection.save(session)

        print(f'Collection "{new_name}" created successfully!')
        return True

    

'''
Function for renaming a collection.
Prompts the user for the new name of the collection.
@param session - object for the current session
@param cid - the ID for the collection to rename
@return True if need to refresh, False if not
'''
def rename_collection(session, cid):
    results, count = Collection.search(cid=cid)

    if (count != 1):
        print("No collection found!")
        return False
    
    current = results[0]

    while (True):
        new_name = input(f'Enter the new name for "{current.name}" [q to quit]')
        if (new_name == ""):
            print("Please enter a name.")
            continue
        if (len(new_name) > 50):
            print("This name is too long!")
            continue
        if (new_name == "q"):
            return False
        
        current.name = new_name
        current.save(session)

        print(f'"{new_name}" updated successfully!')
        return True
    
'''
Refreshes the search list for a user's collections.
This will get called if a user has altered their collections
in some way.
@param uid - the ID for the user's account
@return tuple of results (arr of Collection), count, page 1, max_page
'''
def refresh_collections(uid, per_page):
    results, count = Collection.search(uid=uid, order_by="name")
    max_page = ceil(count / per_page) - 1
    return results, count, max_page


def single_collection_view(session, cid):
    results, count = Collection.search(cid=cid)

    if (count != 1):
        print("No collection found!")
        return False
    
    current = results[0]

    



'''
Function for selecting a collection.
Lists all of the collections owned by a user.
Allows the user to flip thru the pages of collections.
@param session - object for the current session
@param uid - the ID for the user's account
@return idk lol garbage ig
'''
def collection_view(session, uid):
    per_page = 15
    results, count, max_page = refresh_collections(uid, per_page)
    cur_page = 0

    if (count == 0):
        print("No collections found!")
        return False

    while (True):
        # Print the current page
        print("Your collections: ")

        # Prints a page
        # Starts at cur_page, then prints up to per_page entries
        start_index = cur_page * per_page
        for i in range(start_index, start_index + per_page):
            if (i >= count):
                break
            print(f"{i+1}:\t{results[i].name}")

        print(f"Page {cur_page + 1} of {max_page + 1}")

        # Prompt for input
        cmd = input(f'Please enter your command [h for help]')
        
        # Handle numbers differently
        if (cmd.isdigit()):
            
            # convert to int
            index = int(cmd) - 1

            # ensure int is in range
            if ( index < 0 or index >= count ):
                print(f"Please select a value in the range [1, {count}].")
                continue

            # goto the single collection view
            if(single_collection_view(session, results[index].cid)):
                results, count, max_page = refresh_collections(uid, per_page)
                cur_page = 0

            continue

        match cmd:
            case "h":
                print("--- LIST OF COMMANDS ---")
                print("'h' - show the currently available commands")
                print("'q' - return to the previous page")
                print("'c' - create a new collection")
                print("'n' - view the next page")
                print("'p' - view the previous page")
                print("Type a number to view that collection's details.")

            case "q":
                return False
            
            case "c":
                # create_collection will prompt the user to create a new collection
                # once they have created a collection, the program will return here.
                # If create_collection returns true, it means the list of collections
                # needs to be updated.
                if (create_collection(session, uid)):
                    results, count, max_page = refresh_collections(uid, per_page)
                    cur_page = 0

            case "p":
                if (cur_page > 0):
                    cur_page -= 1

            case "n":
                if (cur_page < max_page):
                    cur_page += 1
            
            case _:
                print("Command not recognized.")
    
    print("No collections found!")

    return True
