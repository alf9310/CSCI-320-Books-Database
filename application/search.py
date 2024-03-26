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
        

def search_by_author() -> None:
    # get author
    print("get author") 


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
        
        for results in query_results:
            print(results)
        
        prompt = "Want to keep searching?"
        is_still_searching = utils.ask_continue(prompt) 

def search_by_min_age():
    print("length")


def search_by_max_age():
    print("max_age")