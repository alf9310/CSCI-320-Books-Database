import connect
import utils

def search_title() -> None:
    is_still_searching = True
    while(is_still_searching):
        title = input("What is/are the book(s) titles you are looking for?\n-> ")
        print(f'Your search was, {title}\n')

        # query_statement = f"select * from book where '{title}'|| '%' ilike title order by length(title) desc"
        query_statement = f"SELECT * FROM book WHERE title ILIKE '%{title}%'"
        query_results = connect.execute_query(query_statement) 
        
        for results in query_results:
            print(results)
        
        prompt = "Want to keep searching?"
        is_still_searching = utils.ask_continue(prompt) 
        
 