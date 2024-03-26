import connect
import utils

def search_book() -> None:
    is_still_searching = True
    while(is_still_searching):
        search = input("What is/are the book(s) you are looking for?\n-> ")
        print(f'Your search was, {search}')

        query_results = connect.execute_query("SELECT * FROM book") 
        for results in query_results:
            print(results)
        
        prompt = "Want to keep searching?"
        is_still_searching = utils.ask_continue(prompt) 
        
 