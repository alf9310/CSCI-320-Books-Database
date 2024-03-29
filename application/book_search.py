import connect
import utils

# sswitch to inner when there is more data
SELECT_STATEMENT = "SELECT book.title, author.person_name AS author_name, publisher.person_name AS publisher_name, book.length, book.min_age, book.max_age, AVG(rates.rating)"

def search_by_title() -> None:
    is_still_searching = True
    while(is_still_searching):
        title = utils.get_input_str("What is/are the book(s) titles you are looking for?\n-> ")
        
        print(f'Your search was, {title}\n')

        query_statement = f"\
            {SELECT_STATEMENT} \
            FROM book \
            INNER JOIN written_by \
            ON book.bid = written_by.bid \
            INNER JOIN person author \
            ON written_by.pid = author.pid \
            INNER JOIN published_by \
            ON book.bid = published_by.bid \
            INNER JOIN person publisher \
            ON published_by.pid = publisher.pid \
            INNER JOIN rates \
            ON book.bid = rates.bid \
            INNER JOIN released_as \
            ON book.bid = released_as.bid \
            WHERE title ILIKE '%{title}%' \
            GROUP BY \
            book.title, author.person_name, publisher.person_name, book.length, book.min_age, book.max_age, released_as.date \
            ORDER BY \
            book.title ASC, \
            released_as.date ASC"
            
        query_results = connect.execute_query(query_statement) 
        if query_results: 
            for results in query_results:
                book_title = results[0]
                author = results[1]
                publisher = results[2]
                book_length = results[3]
                book_min_age = results[4]
                book_max_age = results[5]
                book_rating = results[6]
                print(f'{book_title}, {author}, {publisher}, {book_length} pages, {book_min_age}-{book_max_age}, {book_rating:.1f} stars')
        else:
            print("No results")
        
        prompt = "Want to keep searching?"
        is_still_searching = utils.ask_continue(prompt) 
        

def search_by_length():
    is_still_searching = True
    while(is_still_searching):
        min_length_in = utils.get_input_int("What is your desired minimum page amount?\n-> ")
        max_length_in = utils.get_input_int("What is your desired maximum page amount?\n-> ")

        print(f'Your search for books will be between {min_length_in} and {max_length_in} pages\n')

        query_statement = f"\
            SELECT * \
            FROM book \
            WHERE length BETWEEN {min_length_in} AND {max_length_in} \
            ORDER BY length DESC"
        query_results = connect.execute_query(query_statement) 
        if query_results: 
            for results in query_results:
                print(results)
        else:
            print("No results")
        
        prompt = "Want to keep searching?"
        is_still_searching = utils.ask_continue(prompt) 


def search_by_min_age():
    is_still_searching = True
    while(is_still_searching):
        min_age_in = utils.get_input_int("What is your desired minimum age?\n-> ")

        print(f'Your search for books will be targeted towards ages {min_age_in} and older\n')

        query_statement = f"\
            SELECT * \
            FROM book \
            WHERE min_age <= {min_age_in} \
            ORDER BY min_age DESC"
        query_results = connect.execute_query(query_statement) 
        
        if query_results: 
            for results in query_results:
                print(results)
        else:
            print("No results")
        
        prompt = "Want to keep searching?"
        is_still_searching = utils.ask_continue(prompt)


def search_by_max_age():
    is_still_searching = True
    while(is_still_searching):
        max_age_in = utils.get_input_int("What is your desired maximum age?\n-> ")

        print(f'Your search for books will be targeted towards ages {max_age_in} and younger\n')

        query_statement = f"\
            SELECT * \
            FROM book \
            WHERE max_age >= {max_age_in} \
            ORDER BY max_age DESC"
        query_results = connect.execute_query(query_statement) 
        
        if query_results: 
            for results in query_results:
                print(results)
        else:
            print("No results")
         
        prompt = "Want to keep searching?"
        is_still_searching = utils.ask_continue(prompt)
    

def search_by_author() -> None:
    is_still_searching = True
    while(is_still_searching):
        author_name = utils.get_input_str("What wrote the book(s) you are looking for?\n-> ")
        
        print(f'Your search was, {author_name}\n')

        # from person list, find the person that is most like the inputted author
        # then use the gotten persons to link them to the books they wrote
        query_statement = f"\
            {SELECT_STATEMENT} \
            FROM book \
            INNER JOIN written_by \
            ON book.bid = written_by.bid \
            INNER JOIN person author \
            ON written_by.pid = author.pid \
            INNER JOIN published_by \
            ON book.bid = published_by.bid \
            INNER JOIN person publisher \
            ON published_by.pid = publisher.pid \
            INNER JOIN rates \
            ON book.bid = rates.bid \
            INNER JOIN released_as \
            ON book.bid = released_as.bid \
            WHERE author.person_name ILIKE '%{author_name}%' \
            GROUP BY \
            book.title, author.person_name, publisher.person_name, book.length, book.min_age, book.max_age, released_as.date \
            ORDER BY \
            book.title ASC, \
            released_as.date ASC"
        query_results = connect.execute_query(query_statement) 
        if query_results: 
            for results in query_results:
                book_title = results[0]
                author = results[1]
                publisher = results[2]
                book_length = results[3]
                book_min_age = results[4]
                book_max_age = results[5]
                book_rating = results[6]
                print(f'{book_title}, {author}, {publisher}, {book_length} pages, {book_min_age}-{book_max_age}, {book_rating:.1f} stars')
        else:
            print("No results")
        
        prompt = "Want to keep searching?"
        is_still_searching = utils.ask_continue(prompt) 
     

def search_by_published() -> None:
    is_still_searching = True
    while(is_still_searching):
        publisher_name = utils.get_input_str("Who published the book(s) you are looking for?\n-> ")
        
        print(f'Your search was, {publisher_name}\n')

        query_statement = f"\
            {SELECT_STATEMENT} \
            FROM book \
            INNER JOIN written_by \
            ON book.bid = written_by.bid \
            INNER JOIN person author \
            ON written_by.pid = author.pid \
            INNER JOIN published_by \
            ON book.bid = published_by.bid \
            INNER JOIN person publisher \
            ON published_by.pid = publisher.pid \
            INNER JOIN rates \
            ON book.bid = rates.bid \
            INNER JOIN released_as \
            ON book.bid = released_as.bid \
            WHERE publisher.person_name ILIKE '%{publisher_name}%' \
            GROUP BY \
            book.title, author.person_name, publisher.person_name, book.length, book.min_age, book.max_age, released_as.date \
            ORDER BY \
            book.title ASC, \
            released_as.date ASC"
        query_results = connect.execute_query(query_statement) 
        if query_results: 
            for results in query_results:
                book_title = results[0]
                author = results[1]
                publisher = results[2]
                book_length = results[3]
                book_min_age = results[4]
                book_max_age = results[5]
                book_rating = results[6]
                print(f'{book_title}, {author}, {publisher}, {book_length} pages, {book_min_age}-{book_max_age}, {book_rating:.1f} stars')
        else:
            print("No results")
        
        prompt = "Want to keep searching?"
        is_still_searching = utils.ask_continue(prompt) 


def search_by_edited() -> None:
    is_still_searching = True
    while(is_still_searching):
        editor_name = utils.get_input_str("Who edited the book(s) you are looking for?\n-> ")
        
        print(f'Your search was, {editor_name}\n')

        query_statement = f"\
            SELECT book.title, person.person_name \
            FROM book \
            INNER JOIN edited_by \
            ON book.bid = edited_by.bid \
            INNER JOIN person \
            ON person.pid = edited_by.pid \
            WHERE person_name ILIKE '%{editor_name}%' \
            ORDER BY person_name"
        query_results = connect.execute_query(query_statement) 
        if query_results: 
            for results in query_results:
                print(f'{results[0]} edited by {results[1]}')
        else:
            print("No results")
        
        prompt = "Want to keep searching?"
        is_still_searching = utils.ask_continue(prompt) 


# future work, make this able to take in a list? 
def search_by_genre() -> None:
    is_still_searching = True
    while(is_still_searching):
        genre = utils.get_input_str("What is a book genre you are lookiing for?\n-> ")
        
        print(f'Your search was, {genre}\n')

        query_statement = f"\
            {SELECT_STATEMENT}, genre.genre_name \
            FROM book \
            INNER JOIN written_by \
            ON book.bid = written_by.bid \
            INNER JOIN person author \
            ON written_by.pid = author.pid \
            INNER JOIN published_by \
            ON book.bid = published_by.bid \
            INNER JOIN person publisher \
            ON published_by.pid = publisher.pid \
            INNER JOIN rates \
            ON book.bid = rates.bid \
            INNER JOIN released_as \
            ON book.bid = released_as.bid \
            INNER JOIN has_genre \
            ON book.bid = has_genre.bid \
            INNER JOIN genre \
            ON genre.gid = has_genre.gid \
            WHERE genre.genre_name ILIKE '%{genre}%' \
            GROUP BY \
            book.title, author.person_name, publisher.person_name, book.length, book.min_age, book.max_age, released_as.date, genre.genre_name \
            ORDER BY \
            book.title ASC, \
            released_as.date ASC"
        query_results = connect.execute_query(query_statement) 
        if query_results: 
            for results in query_results:
                book_title = results[0]
                author = results[1]
                publisher = results[2]
                book_length = results[3]
                book_min_age = results[4]
                book_max_age = results[5]
                book_rating = results[6]
                book_genre = results[7]
                print(f'{book_genre}: {book_title}, {author}, {publisher}, {book_length} pages, {book_min_age}-{book_max_age}, {book_rating:.1f} stars')
        else:
            print("No results")
        
        prompt = "Want to keep searching?"
        is_still_searching = utils.ask_continue(prompt) 


def search_by_rates() -> None:
    is_still_searching = True
    while(is_still_searching):
        rating = utils.get_input_str("What book rating are you looking for? [1, 2, 3, 4, 5]\n-> ")
        
        print(f'Your search was, {rating}\n')

        # rates contains UID's and their ratings for certain book
        # select all common bids, average their rating, then 
        # select all average bid that is closest to the inputted number
        query_statement = f"\
            SELECT book.title, AVG(rates.rating) AS average_rating \
            FROM book \
            JOIN rates \
            ON book.bid = rates.bid \
            GROUP BY book.bid \
            ORDER BY ABS(AVG(rates.rating) - {rating}) \
            LIMIT 15"
        query_results = connect.execute_query(query_statement) 
        if query_results: 
            for results in query_results:
                print(f'{results[1]:.1f}: {results[0]}')
        else:
            print("No results")
        
        prompt = "Want to keep searching?"
        is_still_searching = utils.ask_continue(prompt) 


def search_release_date() -> None:
    is_still_searching = True
    while(is_still_searching):
        release_date = utils.get_input_str("What is the release date you are looking for? [YYYY-MM-DD]\n-> ")
        
        print(f'Your search was, {release_date}\n')

        # get the release date then order based on alphabetical
        query_statement = f"\
            {SELECT_STATEMENT} \
            FROM book \
            INNER JOIN written_by \
            ON book.bid = written_by.bid \
            INNER JOIN person author \
            ON written_by.pid = author.pid \
            INNER JOIN published_by \
            ON book.bid = published_by.bid \
            INNER JOIN person publisher \
            ON published_by.pid = publisher.pid \
            INNER JOIN rates \
            ON book.bid = rates.bid \
            JOIN released_as \
            ON book.bid = released_as.bid \
            WHERE DATE(released_as.date) = '{release_date}' \
            GROUP BY \
            book.title, author.person_name, publisher.person_name, book.length, book.min_age, book.max_age, released_as.date \
            ORDER BY \
            book.title ASC, \
            released_as.date ASC"
        query_results = connect.execute_query(query_statement) 
        if query_results: 
            for results in query_results:
                book_title = results[0]
                author = results[1]
                publisher = results[2]
                book_length = results[3]
                book_min_age = results[4]
                book_max_age = results[5]
                book_rating = results[6]
                print(f'{book_title}, {author}, {publisher}, {book_length} pages, {book_min_age}-{book_max_age}, {book_rating:.1f} stars')
        else:
            print("No results")
        
        prompt = "Want to keep searching?"
        is_still_searching = utils.ask_continue(prompt) 


def search_format() -> None:
    is_still_searching = True
    while(is_still_searching):
        format = utils.get_input_str("What book format are you looking for? [article/paperback/hardcover/magazine/e-book]\n-> ") 
        print(f'Your search was, {format}\n')

        # get the release date then order based on alphabetical
        query_statement = f"\
            SELECT book.title, format.format_name \
            FROM book \
            JOIN released_as \
            ON book.bid = released_as.bid \
            INNER JOIN format \
            ON released_as.fid = format.fid \
            WHERE format.format_name ILIKE '%{format}%'"
        query_results = connect.execute_query(query_statement) 
        if query_results: 
            for results in query_results:
                print(f'{results[1]}: {results[0]}')
        else:
            print("No results")
        
        prompt = "Want to keep searching?"
        is_still_searching = utils.ask_continue(prompt) 

   
# future work, a generic filter function`