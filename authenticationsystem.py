#Building a Secure Authentication System

import re

def validate_password(password, username, last_three_passwords):
    # Check minimum length
    if len(password) < 10:
        return False, "Password must be at least 10 characters long."
    
    
    # Check character variety
    if not (re.search(r'[A-Z].*[A-Z]', password) and
            re.search(r'[a-z].*[a-z]', password) and
            re.search(r'\d.*\d', password) and
            re.search(r'[!@#$%^&*]+', password)):
        return False, "Password must contain at least two uppercase letters, two lowercase letters, two digits, and two special characters."
    
    
    # Check sequence and repetition restrictions
    if any(username[i:i+3] in password for i in range(len(username) - 2)):
        return False, "Password cannot contain sequences of three or more consecutive characters from the username."
    
    if re.search(r'(.)\1\1\1', password):
        return False, "No character should repeat more than three times in a row."
    
    
    # Check historical password
    if password in last_three_passwords:
        return False, "Password cannot be the same as any of the last three passwords."
    
    return True, "Password meets all criteria."

def main():
    username = input("Enter username: ")
    last_three_passwords = []  
    
    while True:
        password = input("Enter password: ")
        valid, message = validate_password(password, username, last_three_passwords)
        if valid:
            print("Password successfully set.")
            break
        else:
            print("Invalid password:", message)

if __name__ == "__main__":
    main()
