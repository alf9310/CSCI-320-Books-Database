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
        author_name = utils.get_input_str("What is/are the book(s) by some author that you are looking for?\n-> ")
        
        print(f'Your search was, {author_name}\n')

        # from person list, find the person that is most like the inputted author
        # then use the gotten persons to link them to the books they wrote
        query_statement = f"\
            SELECT * \
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
                print(results)
        else:
            print("No results")
        
        prompt = "Want to keep searching?"
        is_still_searching = utils.ask_continue(prompt) 
     

def search_by_published() -> None:
    print("get published")


def search_by_genre() -> None:
    print("search genre")


def search_by_rates() -> None:
    print("search rates")


# future work, a generic filter function