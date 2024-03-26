### Utility file, put any, multipurpose functions in this file to be used
### throughout the application


def ask_continue(prompt: str) -> bool:
    while(True):
        user_in = input("%s [Y/N] " % (prompt))
        if (user_in.upper() == "Y" or user_in.upper() == "YES"): 
            return True
        if (user_in.upper() == "N" or user_in.upper() == "NO"): 
            return False
        print("Invalid input: usage ['Y'/'Yes'/'N'/'No']")