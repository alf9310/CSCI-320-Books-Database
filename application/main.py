import connect
import utils
import search
from users import Users
from friend import Friend

def login(session):
    returning = utils.ask_continue("Are you a returning user?")
    print()
    # Login with existing user
    if returning:
        print("-----Login-----")
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
    # Create a new user
    else:
        print("-----Create New User-----")
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
    # TODO users can loop back to start of function from login & create new user
    # TODO add quit option
    return current_user

def home_page(session, current_user):
    print("\n---------------Home Page---------------")
    print("Find Books")
    print("View Collections")
    print("View Book Logs")
    print("View Friends")
    print("Settings")
    print("Log Out")
    input = utils.get_input_str("-> ")
    print()
    match input:
        case "Find Books":
            find_books()
        case "View Collections":
            view_collections(session, current_user)
        case "View Book Logs":
            view_book_logs(session, current_user)
        case "View Friends":
            view_friends(session, current_user)
        case "Settings":
            settings(session, current_user)
        case "Log Out":
            print("You have been logged out\n")
            login(session)
        case _:
            print("Invalid input, please enter either " + 
                  "\'Find Books\', \'View Collections\', \'View Book Logs\', \'View Friends\', \'Settings\' or \'Log Out\'")

def find_books():
    "---------------Find Books---------------"
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
        case _:
            print("Invalid input, please enter either " + 
                  "\'Find Books\', \'View Collections\', \'View Book Logs\', \'View Friends\' or \'Settings\'")
    # TODO better print format for books 
    # TODO add book view where users can add to collection, add to log, or rate
    return

def view_collections(session, current_user):
    #TODO Search collections by the current user's uid, sort by name in ascending order
    #TODO Show Collections name, Number of books in the collection, Total length of the books (in pages) in the collection
    #TODO Here users can create a new collection, modify the name of a collection & delete an entire collection
    #TODO Collection view, where users can add and delete books from their collection
    #TODO add book view where users can add to current collection, add to log, or rate
    return

def view_book_logs(session, current_user):
    #TODO Search logs by the current user's uid, sort by most recent
    #TODO add book view where users can add to collection, add to log, or rate
    return

def view_friends(session, current_user):
    #TODO Search friends by the current user's uid
    print("Would you like to Friend or Unfriend a user?")
    input = utils.get_input_str("-> ")
    print()
    match input:
        case "Friend":
            Friend.friend_user(session, current_user.uid)
        case "Unfriend":
            Friend.unfriend(session, current_user.uid)
        case _:
            print("Invalid input, please enter either \'Friend\' or \'Unfriend\'")
    return

def settings(session, current_user):
    #TODO users can change email, username, password, etc. or delete account
    return

def main():
    print("---------------BadReads Application Started---------------")
    # Connect to the database
    session = connect.test_connection()

    # Login or create a new account, save current user
    current_user = login(session)

    # Home Page
    print("Welcome to BadReads " + current_user.username + "!")
    home_page(session, current_user)
        

    # ----------------Testing User usage----------------
    '''
    users = session.query(Users).all()
    for user in users:
        print(user)
    print()
    '''

    '''
    # Create a user
    new_user = Users.create(session, first_name = "John", last_name = "Doe", username = "123JohnnyBoy", password = "password123")

    # Query users with the first name John
    results, total_count = Users.search(session, first_name="John")
    print(total_count, "Users with the first name John")
    for result in results:
        print(result)
    print()

    # Query users with the last name Smith
    results, total_count = Users.search(session, last_name="Smith")
    print(total_count, "Users with the last name Smith")
    for result in results:
        print(result)
    print()

    # Update a user
    new_user.last_name = "Smith"
    new_user.save(session)

    # Query users with the last name Smith
    results, total_count = Users.search(session, last_name="Smith")
    print(total_count, "Users with the last name Smith")
    for result in results:
        print(result)
    print()

    # Delete a user
    new_user.delete(session)

    # Query users with the last name Smith
    results, total_count = Users.search(session, last_name="Smith")
    print(total_count, "Users with the last name Smith")
    for result in results:
        print(result)
    print()
    '''


    # ----------------Testing Book Searching----------------
    # search.search_by_title() 
    # search.search_by_length()
    #search.search_by_min_age()
    #search.search_by_max_age()
    # search.search_by_author()
    #search.search_by_genre()
    #search.search_by_edited()
    #search.search_by_published()
    
    session.close()

if __name__ == "__main__":
    main()