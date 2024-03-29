from math import ceil
from book import Book
from users import Users
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
    uid = Column(Integer, ForeignKey(Users.uid))
    name = Column(String)
    date_created = Column(DateTime, default=datetime.now)

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
                f" date_created='{self.date_created}'")
    
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
    new_collection = 0
    
    while (True):
        new_name = input("Please enter the collection name. [q to quit]\n-> ")
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
    results, count = Collection.search(session=session, cid=cid)

    if (count != 1):
        print("No collection found!")
        return False
    
    current = results[0]

    while (True):
        new_name = input(f'Enter the new name for "{current.name}" [q to quit]\n-> ')
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
Removes a book from a collection :))))))
'''
def remove_from_collection(session, cid, bid):
    results, count = In_Collection.search(session=session, cid=cid, bid=bid)

    if (count != 1):
        print("No entry found!")
        return False
    
    current = results[0]

    current.delete(session)

    return True

'''
Attempts to remove a book from a collection but acts real cute about it
'''
def prompt_remove_from_collection(session, cid, bid, c_name, b_title):

    while (True):
        confirm = input(f'Remove {b_title} from {c_name}? [y/n]\n-> ')
        if (confirm == "n"):
            return False
        if (confirm == "y"):
            return remove_from_collection(session, cid, bid)
        print("Input not recognized.")

'''
Attempts to remove a book from a collection but acts real cute about it
'''
def delete_collection(session, current, books, count):

    while (True):
        confirm = input(f'Delete {current.name} permanently? [y/n]\n-> ')
        if (confirm == "n"):
            return False
        if (confirm == "y"):
            # delete all In_Collections first
            for i in range(count):
                remove_from_collection(session, current.cid, books[i].bid)

            current.delete(session)
            return True
        print("Input not recognized.")

'''
Refreshes the search list for a user's collections.
This will get called if a user has altered their collections
in some way.
@param uid - the ID for the user's account
@return tuple of results (arr of Collection), count, page 1, max_page
'''
def refresh_collections(session, uid, per_page):
    results, count = Collection.search(session=session, uid=uid, order_by="name")
    max_page = ceil(count / per_page) - 1
    if (max_page < 0):
        max_page = 0
    return results, count, max_page

'''
Refreshes the search list for the books in a specific collection.
This will get called if a user has altered the collection
in some way.
@param cid - the ID for the collection
@return tuple of results (arr of Books), count, max_page, book_pages
'''
def refresh_in_collection(session, cid, per_page):
    # First getting In_Collection
    res1, c1 = In_Collection.search(session=session, cid=cid)

    # Nothing in collection?
    if (c1 == 0):
        return [], 0, 0, 0
    
    results = []
    book_pages = 0
    # Okey now fetch the Books in this collection
    for i in range(c1):
        b_res, b_count = Book.search(session=session, bid=res1[i].bid)
        
        if (b_count != 1):
            continue
        
        # Add to page count
        book_pages += b_res[0].length

        # Append to book array
        results.append(b_res[0])
    
    max_page = ceil(c1 / per_page) - 1
    return results, c1, max_page, book_pages

def single_collection_view(session, cid):
    results, count = Collection.search(session=session, cid=cid)
    
    current = results[0]

    per_page = 15
    results, count, max_page, book_pages = refresh_in_collection(session, cid, per_page)
    cur_page = 0

    refresh = False

    while (True):
        # Print the current collection
        print(f'Collection "{current.name}"')

        if (count == 0):
            print("There are no books in this collection!")
        else:
            print(f'Number of books: {count}')
            print(f'Total Pages: {book_pages}')

            # Prints a page
            # Starts at cur_page, then prints up to per_page entries
            start_index = cur_page * per_page
            for i in range(start_index, start_index + per_page):
                if (i >= count):
                    break
                print(f"{i+1}:\t{results[i].title}")

        print(f"Page {cur_page + 1} of {max_page + 1}")

        # Prompt for input
        cmd = input(f'\nPlease enter your command [h for help]\n-> ')
        
        # Break down the cmd
        cmd = cmd.split()

        match cmd[0]:
            case "h":
                print("--- LIST OF COMMANDS ---")
                print("'h' - show the currently available commands")
                print("'q' - return to the previous page")
                print("'r' - rename this collection")
                print("'x #' - remove that number (#) book from this collection")
                print("'d' - delete this entire collection")
                print("'n' - view the next page")
                print("'p' - view the previous page")
                print("Type a number to view that collection's details.")

            case "q":
                return refresh
            
            case "r":
                rename_collection(session, cid)

            case "x":
                # Verify number is good
                
                if (cmd[1].isdigit()):
            
                    # no books?
                    if (count == 0):
                        print("No books to remove!")
                        continue

                    # convert to int
                    index = int(cmd[1]) - 1

                    # ensure int is in range
                    if ( index < 0 or index >= count ):
                        print(f"Please select a value in the range [1, {count}].")
                        continue

                    # prompt for confirmation
                    if(prompt_remove_from_collection(session, cid, results[index].bid, current.name, results[index].title)):
                        results, count, max_page, book_pages = refresh_in_collection(session, cid, per_page)
                        cur_page = 0
                        refresh = True                    

                else:
                    # no books?
                    if (count == 0):
                        print("No books to remove!")
                        continue
                    print(f"Please select a value in the range [1, {count}].")

            case "d":
                if (delete_collection(session, current, results, count)):
                    refresh = True
                    return refresh
            
            case "p":
                if (cur_page > 0):
                    cur_page -= 1

            case "n":
                if (cur_page < max_page):
                    cur_page += 1
            
            case _:
                print("Command not recognized.")


'''
Function for selecting a collection.
Lists all of the collections owned by a user.
Allows the user to flip thru the pages of collections.
@param session - object for the current session
@param uid - the ID for the user's account
@return idk lol garbage ig
'''
def view_collections(session, current_user):
    uid = current_user.uid
    per_page = 15
    results, count, max_page = refresh_collections(session, uid, per_page)
    cur_page = 0

    while (True):
        # Print the current page
        print("Your collections: ")

        if (count == 0):
            print("You have no collections!")
        else:
            # Prints a page
            # Starts at cur_page, then prints up to per_page entries
            start_index = cur_page * per_page
            for i in range(start_index, start_index + per_page):
                if (i >= count):
                    break
                print(f"{i+1}:\t{results[i].name}")

        print(f"Page {cur_page + 1} of {max_page + 1}")

        # Prompt for input
        cmd = input(f'\nPlease enter your command [h for help]\n-> ')
        
        # Handle numbers differently
        if (cmd.isdigit()):
            
            # no collections?
            if (count == 0):
                print("Create a collection first!")
                continue

            # convert to int
            index = int(cmd) - 1

            # ensure int is in range
            if ( index < 0 or index >= count ):
                print(f"Please select a value in the range [1, {count}].")
                continue

            # goto the single collection view
            if(single_collection_view(session, results[index].cid)):
                results, count, max_page = refresh_collections(session, uid, per_page)
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
                    results, count, max_page = refresh_collections(session, uid, per_page)
                    cur_page = 0

            case "p":
                if (cur_page > 0):
                    cur_page -= 1

            case "n":
                if (cur_page < max_page):
                    cur_page += 1
            
            case _:
                print("Command not recognized.")