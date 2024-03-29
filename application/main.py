import connect
import utils
from users import Users
from friend import Friend
from book import Book
from rating import Rates

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
            print("Login sucessful")
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
            print("User creation sucessful")
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
    print("Rate Books")
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
        case "Rate Books":
            rate_book(session, current_user)
            home_page(session, current_user)
        case "Log Out":
            print("You have been logged out\n")
            login(session)
        case _:
            print("Invalid input, please enter either " + 
                  "\'Find Books\', \'View Collections\', \'View Book Logs\', \'View Friends\' or \'Log Out\'")
            home_page(session, current_user)
    return

def find_books(session, current_user, query = None):
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
    match input:
        case "Title":
            print("Enter Book Title")
            title = utils.get_input_str("-> ")
            results, total_count = Book.search(session, title=title, query=query)
            print(total_count, "Books found")
            for result in results:
                print(result)
            cont = utils.ask_continue("Would you like to filter this list?")
            if cont:
                find_books(session, current_user, query = query)
        case "Release Date":
            print("Enter Book Minimum Release Date")
            min_release_date = utils.get_input_str("-> ")
            print("Enter Book Maximum Release Date")
            max_release_date = utils.get_input_str("-> ")
            results, total_count = Book.search(session, release_date=[min_release_date, max_release_date], query=query)
            print(total_count, "Books found")
            for result in results:
                print(result)
            cont = utils.ask_continue("Would you like to filter this list?")
            if cont:
                find_books(session, current_user, query = query)
        case "Author":
            print("Enter Book Author")
            author = utils.get_input_str("-> ")
            results, total_count = Book.search(session, author=author, query=query)
            print(total_count, "Books found")
            for result in results:
                print(result)
            cont = utils.ask_continue("Would you like to filter this list?")
            if cont:
                find_books(session, current_user, query = query)
        case "Publisher":
            print("Enter Book Publisher")
            publisher = utils.get_input_str("-> ")
            results, total_count = Book.search(session, publisher=publisher, query=query)
            print(total_count, "Books found")
            for result in results:
                print(result)
            cont = utils.ask_continue("Would you like to filter this list?")
            if cont:
                find_books(session, current_user, query = query)
        case "Genre":
            print("Enter Book Genre")
            genre = utils.get_input_str("-> ")
            results, total_count = Book.search(session, genre=genre, query=query)
            print(total_count, "Books found")
            for result in results:
                print(result)
            cont = utils.ask_continue("Would you like to filter this list?")
            if cont:
                find_books(session, current_user, query = query)
        case "Home Page":
            return
        case _:
            print("Invalid input, please enter either " + 
                  "\'Title\', \'Release Date\', \'Author\', \'Publisher\', \'Genre\' or \'Home Page\'")

        
    '''
    # Old find_books
    print()
    print("---------------Find Books---------------")
    print("What would you like to search for books by? Options:")
    print("Title")
    print("Length")
    print("Minimum Recommended Age")
    print("Maximum Recommended Age")
    print("Author")
    print("Publisher")
    print("Editor")
    print("Genre")
    print("Rating")
    print("Home Page")
    # TODO search by release date
    input = utils.get_input_str("-> ")
    print()
    match input:
        case "Title":
            search.search_by_title()
        case "Length":
            search.search_by_length()
        case "Minimum Recommended Age":
            search.search_by_min_age()
        case "Maximum Recommended Age":
            search.search_by_max_age()
        case "Author":
            search.search_by_author()
        case "Publisher":
            search.search_by_published()
        case "Editor":
            search.search_by_edited()
        case "Genre":
            search.search_by_genre()
        case "Rating":
            search.search_by_rates()
        case "Home Page":
            home_page(session, current_user)
        case _:
            print("Invalid input, please enter either " + 
                  "\'Find Books\', \'View Collections\', \'View Book Logs\' or \'View Friends\'")
    # TODO better print format for books. Label books name, the authors, the publisher, the length, audience and the ratings
    # TODO The list must be sorted alphabetically (ascending) by books name and release date. 
    # TODO Users can sort the resulting list: book name, publisher, genre, and released year (ascending and descending)
    # TODO Not nessesary, bould would be nice to add book view where users can add to collection, add to log, or rate
    '''
    return

def view_collections(session, current_user):
    print()
    print("---------------View Collections---------------")
    #TODO Search collections by the current user's uid, sort by name in ascending order
    #TODO Show Collections name, Number of books in the collection, Total length of the books (in pages) in the collection
    #TODO Here users can create a new collection, modify the name of a collection & delete an entire collection
    #TODO Collection view, where users can add and delete books from their collection
    #TODO add book view where users can add to current collection, add to log, or rate
    return

def view_book_logs(session, current_user):
    print()
    print("---------------View Book Logs---------------")
    #TODO Search logs by the current user's uid, sort by most recent
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
    print("---------------Rate Books---------------")
    print()
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
                            changed_rating = utils.get_input_str("rating (1-5)? ")
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