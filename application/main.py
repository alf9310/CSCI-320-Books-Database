import connect
import utils

from log_book import Log
from math import ceil
from users import Users
from friend import Friend
from book import Book
from collection import view_collections, collection_prompt_add

def login(session):
    print()
    print("Welcome to BadReads! Would you like to: ")
    print("Login")
    print("Create New User")
    print("Quit")
    login_option = utils.get_input_str("-> ")
    print()
    match login_option:
        case "Login": # Login with existing user
            print("---------------Login---------------")
            username = input("Username: ")
            password = input("Password: ")
            results, total_count = Users.search(session, username = username, password = password)
            while total_count == 0:
                print("Incorrect Username and/or Password, please try again")
                username = input("Username: ")
                password = input("Password: ")
                results, total_count = Users.search(session, username = username, password = password)
            current_user = results[0]
            current_user.save(session) # Updates last_accessed
            print("Login successful")
            home_page(session, current_user)
        case "Create New User": # Create a new user
            print("---------------Create New User---------------")
            username = input("Username: ")
            results, total_count = Users.search(session, username = username)
            while total_count > 0: # Makes sure usernames are unique
                print("Username already taken, please enter a new one")
                username = input("Username: ")
                results, total_count = Users.search(session, username = username)
            password = input("Password: ")
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            email = input("Email: ")
            current_user = Users.create(session, first_name = first_name, last_name = last_name, username = username, password = password, email = email)
            print("User creation successful")
            home_page(session, current_user)
        case "Quit": # Quit the program
            return
        case _:
            print("Invalid input, please enter either \'Login\', \'Create New User\' or \'Quit\'")
            login(session)
    # TODO users can loop back to start of function from login & create new user
    return

def home_page(session, current_user):
    print()
    print("---------------Home Page---------------")
    print("Find Books")
    print("View Collections")
    print("View Book Logs")
    print("View Friends")
    print("Log Out")
    input = utils.get_input_str("-> ")
    print()
    match input:
        case "Find Books":
            find_books(session, current_user)
            home_page(session, current_user)
        case "View Collections":
            view_collections(session, current_user)
            home_page(session, current_user)
        case "View Book Logs":
            view_book_logs(session, current_user)
            home_page(session, current_user)
        case "View Friends":
            view_friends(session, current_user)
            home_page(session, current_user)
        case "Log Out":
            print("You have been logged out\n")
            login(session)
        case _:
            print("Invalid input, please enter either " + 
                  "\'Find Books\', \'View Collections\', \'View Book Logs\', \'View Friends\' or \'Log Out\'")
            home_page(session, current_user)
    return

'''
Displays the results of the current book query.
From this function, users can:
Rate books
Log books
Collect books
Sort the results
'''
def results_view(session, current_user, query, count):
    
    per_page = 15
    max_page = ceil(count / per_page) - 1
    cur_page = 0

    #no results!
    if (count <= 0):
        print("No books found.\nTry a different search!")
        return

    while (True):
        # Print the current page
        print("--- SEARCH RESULTS ---")
        print(count, "Books found")

        # Prints a page
        # Starts at cur_page, then prints up to per_page entries
        start_index = cur_page * per_page
        for i in range(start_index, start_index + per_page):
            if (i >= count):
                break
            print(f"{i+1}:\t{query[i]}")
            # TODO books need to show ratings

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
                print("'s' - sort the current results")
                print("'c #' - add that book to one of your collections")
                print("'r #' - give that book a rating")
                print("'l #' - add that book to your logs")
                print("'n' - view the next page")
                print("'p' - view the previous page")

            case "q":
                return True
            
            case "s":
                #TODO: Sort stuff here!
                # Sorting should prompt the user for:
                # the attribute name to sort by
                # and
                # ASC or DESC (ascending or descending)
                # it should alter the "query" variable in the scope
                # of THIS function

                # also sets the current page back to 0 >:]
                cur_page = 0
                continue

            case "c":
                # Verify number is good
                
                if (cmd[1].isdigit()):

                    # convert to int
                    index = int(cmd[1]) - 1

                    # ensure int is in range
                    if ( index < 0 or index >= count ):
                        print(f"Please select a value in the range [1, {count}].")
                        continue
                    
                    #TODO: Add to collection function here!
                    collection_prompt_add(session, current_user, query[index])
                    continue              

                else:
                    print(f"Please select a value in the range [1, {count}].")
            
            case "r":
                # Rating stuff here!

                # Verify number is good
                if (cmd[1].isdigit()):

                    # convert to int
                    index = int(cmd[1]) - 1

                    # ensure int is in range
                    if ( index < 0 or index >= count ):
                        print(f"Please select a value in the range [1, {count}].")
                        continue
                    
                    #TODO: Add rating function here!
                    # Should accept:
                    #   current_user, which is a user obj for the person logged in
                    #   query[index], which is a book obj for the selected book
                    #   session, which is used to save the changes made by this function
                    # Simply return out of the function to return here.
                    # Ideally, this function prompts the user for a number 1-5
                    # to rate the book, or display the current rating if the
                    # user has already rated this book. Ratings can be updated.
                    continue              

                else:
                    print(f"Please select a value in the range [1, {count}].")

            case "l":
                # Log stuff here!

                # Verify number is good
                if (cmd[1].isdigit()):

                    # convert to int
                    index = int(cmd[1]) - 1

                    # ensure int is in range
                    if ( index < 0 or index >= count ):
                        print(f"Please select a value in the range [1, {count}].")
                        continue
                    
                    #TODO: Add log function here!
                    # Should accept:
                    #   current_user, which is a user obj for the person logged in
                    #   query[index], which is a book obj for the selected book
                    #   session, which is used to save the changes made by this function
                    # Simply return out of the function to return here.
                    # Ideally, this function prompts the user for a start page,
                    # end page, start time, and end time.
                    continue              

                else:
                    print(f"Please select a value in the range [1, {count}].")

            case "p":
                if (cur_page > 0):
                    cur_page -= 1

            case "n":
                if (cur_page < max_page):
                    cur_page += 1
            
            case _:
                print("Command not recognized.")


def find_books(session, current_user):
    while (True):
        print()
        print("---------------Find Books---------------")
        print("What would you like to search for books by? Options:")
        print("Title")
        print("Release Date")
        print("Author")
        print("Publisher")
        print("Genre")
        print("Home Page")
        input = utils.get_input_str("-> ")
        print()

        query = []

        # get all results from search criteria
        match input:
            case "Title":
                print("Enter Book Title")
                title = utils.get_input_str("-> ")
                query, total_count = Book.search(session, title=title, order_by="title")

            case "Release Date":
                print("Enter Book Minimum Release Date")
                min_release_date = utils.get_input_str("-> ")
                print("Enter Book Maximum Release Date")
                max_release_date = utils.get_input_str("-> ")
                query, total_count = Book.search(session, release_date=[min_release_date, max_release_date], order_by="title")

            case "Author":
                print("Enter Book Author")
                author = utils.get_input_str("-> ")
                query, total_count = Book.search(session, author=author, order_by="title")

            case "Publisher":
                print("Enter Book Publisher")
                publisher = utils.get_input_str("-> ")
                query, total_count = Book.search(session, publisher=publisher, order_by="title")

            case "Genre":
                print("Enter Book Genre")
                genre = utils.get_input_str("-> ")
                query, total_count = Book.search(session, genre=genre, order_by="title")

            case "Home Page":
                return

            case _:
                print("Invalid input, please enter either " + 
                      "\'Title\', \'Release Date\', \'Author\', \'Publisher\', \'Genre\' or \'Home Page\'")

        #ok now print the results
        results_view(session, current_user, query, total_count)

    # TODO The list must be sorted alphabetically (ascending) by books name and release date. 
    # TODO Users can sort the resulting list: book name, publisher, genre, and released year (ascending and descending)
    return

def view_book_logs(session, current_user):
    print()
    print("---------------View Book Logs---------------")
    #TODO Search logs by the current user's uid, sort by most recent
    # display all the logs this user currently has
    Log.listLogs(session, current_user.uid)
    print()
    user_in = utils.ask_continue("Would you like to record a new log?")
    if user_in:
        title = utils.get_input_str("\nWhat book would you like to log?\n-> ")
        bookID = (session.query(Book).filter_by(title=title).order_by(Book.title).first()).bid
        start_time = utils.get_date_str("start time?")
        end_time = utils.get_date_str("end time?")
        start_page = utils.get_input_int("\nstart page?\n-> ")
        end_page = utils.get_input_int("\nend page?\n-> ")
        Log.create(session, bookID, current_user.uid, start_time, end_time, start_page, end_page)
    #TODO add book view where users can add to collection, add to log, or rate
    return

def view_friends(session, current_user):
    print()
    print("---------------View Friends---------------")
    Friend.listFriends(session, current_user.uid)
    print()
    print("Would you like to Friend or Unfriend a user, or return to the Home Page?")
    input = utils.get_input_str("-> ")
    print()
    match input:
        case "Friend":
            Friend.friend_user(session, current_user.uid)
            view_friends(session, current_user)
        case "Unfriend":
            Friend.unfriend(session, current_user.uid)
            view_friends(session, current_user)
        case "Home Page":
            return
        case _:
            print("Invalid input, please enter either \'Friend\', \'Unfriend\' or \'Home Page\'")
            view_friends(session, current_user)
    return

def main():
    print("---------------BadReads Application Started---------------")
    # Connect to the database
    session = connect.test_connection()

    # Login or create a new account, save current user
    login(session)
    print("Disconnecting From Database")
    session.close()

if __name__ == "__main__":
    main()