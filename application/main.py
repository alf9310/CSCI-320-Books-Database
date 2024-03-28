import connect
import utils
import search
from users import Users

def main():
    print("---------------BadReads Application Started---------------")
    # Connect to the database
    session = connect.test_connection()

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
        email = input("Email: ")                          #TODO impliment email saving
        while(utils.ask_continue("Would you like to input another email?")):
            email = input("Email: ")
        current_user = Users.create(session, first_name = first_name, last_name = last_name, username = username, password = password)
        print("User creation sucessful")
        

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
    #search.search_by_author()

    session.close()

if __name__ == "__main__":
    main()