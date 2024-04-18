from users import Users
from friend import Friend
from book import Book, Rates
from log_book import Log

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.sql.expression import func

Base = declarative_base()

'''
Calculates the "popularity" value of a given book.
Popularity = avg_rating * (number_of_recent_logs)^1.2
'''
def calculate_popularity_time( session, book, time_filter ):
    avg_rating = Rates.get_average_rating(session, book.bid)

    # No Ratings yet?
    if (avg_rating == "-"):
        return 0
    else:
        # convert from string to float
        avg_rating = float(avg_rating)

    if (avg_rating < 3):
        return 0
    
    results = False
    count = False

    # Was a time provided?
    if (time_filter and isinstance(time_filter, datetime)):
        # Any log BEFORE time_filter is ignored
        results, count = Log.search(session=session, bid=book.bid, start_time=time_filter)
    else:
        results, count = Log.search(session=session, bid=book.bid) 

    # Default val if something goes wrong / no recent logs
    if (not count):
        return 0

    return count * avg_rating * avg_rating

'''
Displays the top 20 books from the past
90 days
'''
def recently_popular_books( session ):
    
    print("Please wait...")
    
    # Create a blank array for the books and their popularity
    arr = [[-1 for i in range(2)] for j in range(20)]

    # Query is ALL books
    query, count = Book.search(session)

    # 90 days ago
    time_filter = datetime.now() - timedelta(days=90)

    for book in query:
        
        popularity = calculate_popularity_time(session, book, time_filter)
        
        if (popularity <= 0):
            continue

        # arr holds the top 20 books in order,
        # column 1 is the book instance,
        # column 2 is the popularity rating

        # goes from index 0 to index 19
        for i in range(20):
            if (popularity > arr[i][1]):
                if (i > 0):
                    # move the current one back
                    arr[i-1][0] = arr[i][0]
                    arr[i-1][1] = arr[i][1]
                # replace
                arr[i][0] = book
                arr[i][1] = popularity
            else:
                break

    # Now display
    print("---- 90-Day Trending Books ----")
    for i in reversed(range(20)):
        string_rep = arr[i][0].__str__(session)
        print(f"#{20-i} :\t{string_rep}")

        

