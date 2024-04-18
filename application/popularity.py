
from book import Book, Rates
from sqlalchemy.orm import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.sql.expression import func
from sqlalchemy.sql import text

Base = declarative_base()

'''
Calculates the "popularity" value of a given book.
Popularity = avg_rating^3 * number_of_recent_logs
'''
def calculate_popularity( log_count, avg_rating ):
    return log_count * avg_rating * avg_rating * avg_rating

'''
Displays the top 20 books from the past
90 days

'''
def recently_popular_books( session ):
    
    print("Calculating popularity...")
    
    # Create a blank array for the books and their popularity
    arr = [[-1 for i in range(2)] for j in range(20)]

    # 90 days ago
    time_filter = datetime.now() - timedelta(days=90)

    # Get logs within the past 90 days
    book_occurrence = session.execute(text(f"""SELECT bid, COUNT(*) AS log_count
    FROM logs
    WHERE start_time >= '{time_filter.strftime('%Y-%m-%d %H:%M:%S')}'
    GROUP BY bid""")).all()

    for i in range(len(book_occurrence)):

        # Get the avg
        avg_rating = session.query(func.avg(Rates.rating).label('average')).filter(Rates.bid==book_occurrence[i][0])     
        avg_rating = session.execute(avg_rating).first()[0]
        
        popularity = calculate_popularity(book_occurrence[i][1], avg_rating)

        # arr holds the top 20 books in order,
        # column 1 is the book id,
        # column 2 is the popularity rating

        # goes from index 0 to index 19
        for k in range(20):
            if (popularity > arr[k][1]):
                if (k > 0):
                    # move the current one back
                    arr[k-1][0] = arr[k][0]
                    arr[k-1][1] = arr[k][1]
                # replace
                arr[k][0] = book_occurrence[i][0]
                arr[k][1] = popularity
            else:
                break

    # Now display
    print("---- 90-Day Trending Books ----")
    for i in reversed(range(20)):
        if (arr[i][0] == -1):
            break
        b_query, b_count = Book.search(session=session, bid=arr[i][0])
        string_rep = b_query[0].__str__(session)
        print(f"#{20-i} :\t{string_rep}")

"""
Displays the top 20 books among my friends.
"""        
def friend_popular_books( session, current_user ):
    
    print("Calculating popularity...")
    
    # Create a blank array for the books and their popularity
    arr = [[-1 for i in range(2)] for j in range(20)]

    # 90 days ago
    time_filter = datetime.now() - timedelta(days=90)

    # Get logs within the past 90 days
    book_occurrence = session.execute(text(f"""SELECT l.bid, COUNT(*) AS friend_log_count
        FROM logs AS l
        JOIN friend AS f ON l.uid = f.friend_id
        WHERE f.uid = {current_user.uid}
        GROUP BY l.bid;""")).all()

    for i in range(len(book_occurrence)):

        # Get the avg
        avg_rating = session.query(func.avg(Rates.rating).label('average')).filter(Rates.bid==book_occurrence[i][0])     
        avg_rating = session.execute(avg_rating).first()[0]
        
        popularity = calculate_popularity(book_occurrence[i][1], avg_rating)

        # arr holds the top 20 books in order,
        # column 1 is the book id,
        # column 2 is the popularity rating

        # goes from index 0 to index 19
        for k in range(20):
            if (popularity > arr[k][1]):
                if (k > 0):
                    # move the current one back
                    arr[k-1][0] = arr[k][0]
                    arr[k-1][1] = arr[k][1]
                # replace
                arr[k][0] = book_occurrence[i][0]
                arr[k][1] = popularity
            else:
                break

    # Now display
    print("---- Trending Books Among My Friends ----")
    for i in reversed(range(20)):
        if (arr[i][0] == -1):
            break
        b_query, b_count = Book.search(session=session, bid=arr[i][0])
        string_rep = b_query[0].__str__(session)
        print(f"#{20-i} :\t{string_rep}")

"""
Calculates and displays the top 5 new releases of
this month
"""
def popular_new_releases( session ):
    print("Calculating popularity...")
    
    # Create a blank array for the books and their popularity
    arr = [[-1 for i in range(2)] for j in range(5)]

    # This month
    this_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    temp_mon = (this_month.month) % 12 + 1
    next_month = this_month.replace(month=temp_mon)

    # Get count of 
    book_occurrence = session.execute(text(f"""SELECT l.bid, COUNT(*) AS log_count
    FROM logs AS l
    JOIN released_as AS r ON l.bid = r.bid
    WHERE l.start_time BETWEEN '{this_month.strftime('%Y-%m-%d %H:%M:%S')}' AND '{next_month.strftime('%Y-%m-%d %H:%M:%S')}'
    AND r.date BETWEEN '{this_month.strftime('%Y-%m-%d %H:%M:%S')}' AND '{next_month.strftime('%Y-%m-%d %H:%M:%S')}'
    GROUP BY l.bid""")).all()

    for i in range(len(book_occurrence)):

        # Get the avg
        avg_rating = session.query(func.avg(Rates.rating).label('average')).filter(Rates.bid==book_occurrence[i][0])     
        avg_rating = session.execute(avg_rating).first()[0]
        
        popularity = calculate_popularity(book_occurrence[i][1], avg_rating)

        # arr holds the top 20 books in order,
        # column 1 is the book id,
        # column 2 is the popularity rating

        # goes from index 0 to index 4
        for k in range(5):
            if (popularity > arr[k][1]):
                if (k > 0):
                    # move the current one back
                    arr[k-1][0] = arr[k][0]
                    arr[k-1][1] = arr[k][1]
                # replace
                arr[k][0] = book_occurrence[i][0]
                arr[k][1] = popularity
            else:
                break

    # Now display
    print("---- Popular New Releases ----")
    for i in reversed(range(5)):
        if (arr[i][0] == -1):
            break
        b_query, b_count = Book.search(session=session, bid=arr[i][0])
        string_rep = b_query[0].__str__(session)
        print(f"#{5-i} :\t{string_rep}")