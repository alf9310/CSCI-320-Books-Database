import connect
import utils
from users import Users
from friend import Friend
from book import Book

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

def find_books(session, current_user, descending = False, query = None):
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
            query, total_count = Book.search(session, title=title, order_by="title", descending = descending, query=query)
            print(total_count, "Books found")
            for result in query:
                print(result)
                print()
            cont = utils.ask_continue("Would you like to filter this list?")
            if cont:
                descending = utils.ask_continue("Would you like to sort by descending order?")
                print("Filtering List")
                find_books(session, current_user, descending = descending, query = query)
            else:
                find_books(session, current_user)
        case "Release Date":
            print("Enter Book Minimum Release Date")
            min_release_date = utils.get_input_str("-> ")
            print("Enter Book Maximum Release Date")
            max_release_date = utils.get_input_str("-> ")
            query, total_count = Book.search(session, release_date=[min_release_date, max_release_date], order_by="title", descending = descending, query=query)
            print(total_count, "Books found")
            for result in query:
                print(result)
                print()
            cont = utils.ask_continue("Would you like to filter this list?")
            if cont:
                descending = utils.ask_continue("Would you like to sort by descending order?")
                print("Filtering List")
                find_books(session, current_user, descending = descending, query = query)
            else:
                find_books(session, current_user)
        case "Author":
            print("Enter Book Author")
            author = utils.get_input_str("-> ")
            query, total_count = Book.search(session, author=author, order_by="title", descending = descending, query=query)
            print(total_count, "Books found")
            for result in query:
                print(result)
                print()
            cont = utils.ask_continue("Would you like to filter this list?")
            if cont:
                descending = utils.ask_continue("Would you like to sort by descending order?")
                print("Filtering List")
                find_books(session, current_user, descending = descending, query = query)
            else:
                find_books(session, current_user)
        case "Publisher":
            print("Enter Book Publisher")
            publisher = utils.get_input_str("-> ")
            query, total_count = Book.search(session, publisher=publisher, order_by="title", descending = descending, query=query)
            print(total_count, "Books found")
            for result in query:
                print(result)
                print()
            cont = utils.ask_continue("Would you like to filter this list?")
            if cont:
                descending = utils.ask_continue("Would you like to sort by descending order?")
                print("Filtering List")
                find_books(session, current_user, descending = descending, query = query)
            else:
                find_books(session, current_user)
        case "Genre":
            print("Enter Book Genre")
            genre = utils.get_input_str("-> ")
            query, total_count = Book.search(session, genre=genre, order_by="title", descending = descending, query=query)
            print(total_count, "Books found")
            for result in query:
                print(result)
                print()
            cont = utils.ask_continue("Would you like to filter this list?")
            if cont:
                descending = utils.ask_continue("Would you like to sort by descending order?")
                print("Filtering List")
                find_books(session, current_user, descending = descending, query = query)
            else:
                find_books(session, current_user)
        case "Home Page":
            return
        case _:
            print("Invalid input, please enter either " + 
                  "\'Title\', \'Release Date\', \'Author\', \'Publisher\', \'Genre\' or \'Home Page\'")

    # TODO books need to show ratings
    # TODO The list must be sorted alphabetically (ascending) by books name and release date. 
    # TODO Users can sort the resulting list: book name, publisher, genre, and released year (ascending and descending)
    # TODO Not nessesary, bould would be nice to add book view where users can add to collection, add to log, or rate
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