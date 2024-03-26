### Utility file, put any, multipurpose functions in this file to be used
### throughout the application

### takes in a prompt and asks user if they want to continue or not
### this can be used in functions where users have the option to keep
### doing an action such as searching
def ask_continue(prompt: str) -> bool:
    while(True):
        user_in = input(f'\n{prompt} [y/n]\n-> ')
        if (user_in.upper() == "Y" or user_in.upper() == "YES"): 
            return True
        if (user_in.upper() == "N" or user_in.upper() == "NO"): 
            return False
        print("Invalid input: usage [y/n/Yes/No/Y/N]")


def get_input_str(message: str) -> str:
    user_in = ""
    invalid_list = [""]
    while (True):
        user_in = input(message)
        if user_in in invalid_list: 
            print("invalid input")
        else:
            break
    return user_in


def get_input_int(message: str) -> str:
    user_in = ""
    invalid_list = [""]
    while (True):
        user_in = input(message)
        if user_in in invalid_list or not user_in.isnumeric(): 
            print("invalid number")
        else:
            break
    return user_in
