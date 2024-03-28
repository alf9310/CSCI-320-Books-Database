import connect
import utils

def search_by_title() -> None:
    is_still_searching = True
    while(is_still_searching):
        title = utils.get_input_str("What is/are the book(s) titles you are looking for?\n-> ")
        
        print(f'Your search was, {title}\n')

        query_statement = f"\
            SELECT * \
            FROM book \
            WHERE title ILIKE '%{title}%'"
        query_results = connect.execute_query(query_statement) 
        if query_results: 
            for results in query_results:
                print(results)
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
            SELECT book.title, person.person_name \
            FROM book \
            INNER JOIN written_by \
            ON book.bid = written_by.bid \
            INNER JOIN person \
            ON person.pid = written_by.pid \
            WHERE person_name ILIKE '%{author_name}%' \
            ORDER BY person_name"
        query_results = connect.execute_query(query_statement) 
        if query_results: 
            for results in query_results:
                print(f'{results[0]} by {results[1]}')
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
            SELECT book.title, person.person_name \
            FROM book \
            INNER JOIN published_by \
            ON book.bid = published_by.bid \
            INNER JOIN person \
            ON person.pid = published_by.pid \
            WHERE person_name ILIKE '%{publisher_name}%' \
            ORDER BY person_name"
        query_results = connect.execute_query(query_statement) 
        if query_results: 
            for results in query_results:
                print(f'{results[0]} edited by {results[1]}')
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
            SELECT book.title, genre.genre_name \
            FROM book \
            INNER JOIN has_genre \
            ON book.bid = has_genre.bid \
            INNER JOIN genre \
            ON genre.gid = has_genre.gid \
            WHERE genre.genre_name ILIKE '%{genre}%' \
            ORDER BY genre.genre_name"
        query_results = connect.execute_query(query_statement) 
        if query_results: 
            for results in query_results:
                print(f'{results[1]}:  {results[0]}')
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
                print(f'{results[1]:.1f}:  {results[0]}')
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
            SELECT book.title, released_as.date \
            FROM book \
            JOIN released_as \
            ON book.bid = released_as.bid \
            WHERE  DATE(released_as.date) = '{release_date}'"
        query_results = connect.execute_query(query_statement) 
        if query_results: 
            for results in query_results:
                print(f'{results[1]}:  {results[0]}')
        else:
            print("No results")
        
        prompt = "Want to keep searching?"
        is_still_searching = utils.ask_continue(prompt) 


def search_format() -> None:
    print("get format")
   
# future work, a generic filter function`