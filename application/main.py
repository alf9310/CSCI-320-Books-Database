import connect
import utils

from log_book import Log
from math import ceil
from users import Users
from friend import Friend
from popularity import recently_popular_books
from book import Book, Rates
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
    print("View Ratings")
    print("Popular Books")
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
        case "View Ratings":
            rate_book(session, current_user)
            home_page(session, current_user)
        case "Popular Books":
            popular_books(session, current_user)
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

    print_search_flag = True
    while (True):
        if print_search_flag:
            # Print the current page
            print("--- SEARCH RESULTS ---")
            print(count, "Books found")

            # Prints a page
            # Starts at cur_page, then prints up to per_page entries
            start_index = cur_page * per_page
            for i in range(start_index, start_index + per_page):
                if (i >= count):
                    break
                string_rep = query[i].__str__(session)
                print(f"{i+1}:\t{string_rep}")
                # TODO books need to show ratings

            print(f"Page {cur_page + 1} of {max_page + 1}")
            print_search_flag = False

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
                # the attribute name to sort by (book name, publisher, genre, and released year)
                # and
                # ASC or DESC (ascending or descending)
                # it should alter the "query" variable in the scope
                # of THIS function
                order_by = "na"
                descending = False
                attributes = ("Title", "Publisher", "Genre", "Released Year")
                
                while True:
                    print("What would you like to sort by? [q to quit]")
                    
                    for i, attribute in enumerate(attributes):
                        print(f"{i+1}:\t{attribute}")
                    
                    sort_attribute = utils.get_input_int("-> ")
                    
                    match sort_attribute:
                        case "1":
                            order_by = "title"
                        case "2":
                            order_by = "publisher"
                        case "3":
                            order_by = "genre"
                        case "4":
                            order_by = "release_year"
                        case "q":
                            break
                        case _:
                            print(f"Please select a value in the range [1, {len(attributes)}].")
                            continue
                    
                    break
                
                if (order_by == "na"):
                    # exit the warrior
                    # todays tom sawyer
                    continue
                    
                print("Would you like to sort in ascending or descending order?")
                print("1:\tAscending")
                print("2:\tDescending")
                sort_order = utils.get_input_int("-> ")
                
                while True:
                    match sort_order:
                        case "1":
                            descending = False
                        case "2":
                            descending = True
                        case _:
                            print(f"Please select a value in the range [1, 2].")
                            continue
                    break
                
                # order_by has attribute,
                # descending has sort order
                query, count = Book.search(session, query = query, order_by=order_by, descending=descending)

                # also sets the current page back to 0 >:]
                cur_page = 0
                print_search_flag = True
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
                if (len(cmd) == 2 and cmd[1].isdigit()):

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

                    ratings, rating_count = Rates.search(session, uid=current_user.uid, bid=query[index].bid)
                    if(rating_count > 0):
                        print("You have given", query[index].title, "a rating of", ratings.first().rating)
                        confirm = utils.ask_continue("Would you like to change rating?")
                        if (confirm):
                            while (True):
                                try:
                                    changed_rating = utils.get_input_str("Enter the new rating (1-5)? ")
                                    new_rating_int = int(changed_rating)
                                    break
                                except Exception as e:
                                    print("Invalid Rating")
                                    continue
                            Rates.change_rating(session, current_user.uid, query[index].bid, new_rating_int)
                            print("Updated successfully!")
                    else:
                        while (True):
                            try:
                                rating = utils.get_input_str("What is your rating (1-5)? ")
                                rating_int = int(rating)
                                break
                            except Exception as e:
                                print("Invalid Rating")
                                continue
                        Rates.create(session, current_user.uid, query[index].bid, rating_int)
                        print("Rated successfully!")
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

                    start_time = utils.get_date_str("start time?")
                    end_time = utils.get_date_str("end time?")
                    start_page = utils.get_input_int("\nstart page?\n-> ")
                    end_page = utils.get_input_int("\nend page?\n-> ")
                    Log.create(session, query[index], current_user.uid, start_time, end_time, start_page, end_page)
                    continue              

                else:
                    print(f"Please select a value in the range [1, {count}].")

            case "p":
                if (cur_page > 0):
                    cur_page -= 1
                print_search_flag = True
            case "n":
                if (cur_page < max_page):
                    cur_page += 1
                print_search_flag = True
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
        print()

        query = []

        # get all results from search criteria
        
        match utils.get_find_book_filter("Please enter your search"):
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

        #ok now print the results
        results_view(session, current_user, query, total_count)

    # TODO The list must be sorted alphabetically (ascending) by books name and release date. 
    # TODO Users can sort the resulting list: book name, publisher, genre, and released year (ascending and descending)
    return

def popular_books(session, current_user):
    
    while (True):
        print()
        print("------------Popular Books------------")
        print("Which category would you like? Options:")
        print("1:\tLast 90 Days")
        print("2:\tAmong My Friends")
        print("3:\tNew Releases")
        print("4:\tRecommended For Me")
        print("5:\tReturn to Home Page")
        print()
        
        match utils.get_input_str("Please enter your selection [1-5]\n-> "):
            case "1":
                recently_popular_books(session)
                return

            case "5":
                return

def view_book_logs(session, current_user):
    print()
    print("---------------View Book Logs---------------")
    #TODO Search logs by the current user's uid, sort by most recent
    # display all the logs this user currently has
    Log.list_logs(session, current_user.uid)
    print()
    return
    user_in = utils.ask_continue("Would you like to record a new log?")
    if user_in:
        title = utils.get_input_str("\nWhat book would you like to log?\n-> ")
        bookID = Book.search(session, title=title)[0][0].bid
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

def rate_book(session, current_user):
    print()
    print("---------------Book Ratings ---------------")
    print()
    Rates.rating_view(session, current_user.uid)
    return
    
    print("Would you like to Rate Book or View Ratings? ")
    first_input = utils.get_input_str("-> ")
    match first_input:
        case "Rate Book":
            print("Select book you would like to rate")
            input = utils.get_input_str("-> ")
            try:
                book_id = (session.query(Book).filter_by(title=input).order_by(Book.title).first()).bid
            except Exception as e:
                print("Invalid Book Title")
                session.rollback()
                return
            user_id = (current_user.uid)
            results, total_count = Rates.search(session, uid=user_id, bid=book_id)
            if(total_count > 0):
                print("You have given", input, "a rating of", results.first().rating)
                print("Would you like to change rating? (y/n)")
                new_input = utils.get_input_str("-> ")
                match new_input:
                    case "y":
                        try:
                            changed_rating = utils.get_input_str("What would you like to rate this book! (1-5)? ")
                            new_rating_int = int(changed_rating)
                        except Exception as e:
                            print("Invalid Rating")
                            return
                        Rates.change_rating(session, user_id, book_id, new_rating_int)
                        return
                    case "n":
                        return
                    case _:
                        return
                return
            else:
                try:
                    rating = utils.get_input_str("rating (1-5)? ")
                    rating_int = int(rating)
                except Exception as e:
                    print("Invalid Rating")
                    return
                Rates.create(session, user_id, book_id, rating_int)
                return
        case "View Ratings":
            Rates.rating_view(session, current_user.uid)
            return
        case _:
            print("Invalid input")
            return
        

    print("Select book you would like to rate")
    input = utils.get_input_str("-> ")
    book_id = (session.query(Book).filter_by(title=input).order_by(Book.title).first()).bid
    user_id = (current_user.uid)
    results, total_count = Rates.search(session, uid=user_id, bid=book_id)
    if(total_count > 0):
        print("You have given", input, "a rating of", results.first().rating)
        print("Would you like to change rating? (y/n)")
        new_input = utils.get_input_str("-> ")
        match new_input:
            case "y":
                changed_rating = utils.get_input_str("rating? ")
                new_rating_int = int(changed_rating)
                Rates.change_rating(session, user_id, book_id, new_rating_int)
                return
            case "n":
                return
            case _:
                return
        return
    else:
        rating = utils.get_input_str("rating? ")
        rating_int = int(rating)
        Rates.create(session, user_id, book_id, rating_int)
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