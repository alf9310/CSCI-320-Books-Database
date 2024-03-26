### Utility file, put any, multipurpose functions in this file to be used
### throughout the application

### takes in a prompt and asks user if they want to continue or not
### this can be used in functions where users have the option to keep
### doing an action such as searching
def ask_continue(prompt: str) -> bool:
    while(True):
        user_in = input(f'\n{prompt} Y/Yes/y | N/No/n\n-> ')
        if (user_in.upper() == "Y" or user_in.upper() == "YES"): 
            return True
        if (user_in.upper() == "N" or user_in.upper() == "NO"): 
            return False
        print("Invalid input: usage Y/Yes/N/No")