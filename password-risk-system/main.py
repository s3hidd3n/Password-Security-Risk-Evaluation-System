

import getpass
import hashlib
import requests
import guessability

#Creating an empty leaked password list 

leaked_password = [] 

with open ("/Users/saheed/Desktop/main project/data/100k-most-used-passwords-NCSC.txt","r", encoding="utf-8", errors="ignore") as file:
    for line in file:
        leaked_password.append(line.strip())


with open ("/Users/saheed/Desktop/main project/data/rockyou.txt", "r", encoding="utf-8", errors="ignore") as file:
    for line in file: 
        leaked_password.append(line.strip())


with open ("/Users/saheed/Desktop/main project/data/xato-net-10-million-passwords.txt", "r", encoding="utf-8", errors="ignore") as file:
    for line in file:
        leaked_password.append(line.strip())



#Creating an online check using k-anonymity

def online_check(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()

    prefix = sha1[:5]
    suffix = sha1[5:]

    #Sending the first 5 characters to the API

    url = "https://api.pwnedpasswords.com/range/" + prefix 

    response = requests.get(url, timeout= 5)

    for line in response.text.splitlines():
        parts = line.split(":")

        returned_suffix = parts[0]
        count = parts[1]

        if returned_suffix == suffix:
            return int(count)
        
    return 0
        
warning_message = """
Security Warning: This password has been found in known data breaches. If you have used this password anywhere, you should change it immediately.

Tips for creating a strong password (NIST-compliant):

• Use at least 12 characters (16 or more is recommended)
• Longer passwords are stronger than shorter, complex passwords
• You may use:
  - Uppercase letters (A-Z)
  - Lowercase letters (a-z)
  - Numbers (0-9)
  - Special characters (! @ # $ % etc.)
  - Spaces are also allowed

• Consider using a passphrase made of multiple random words

After changing your password, please enter the new password again to run another security check.

This guidance follows NIST SP 800-63B Digital Identity Guidelines.
"""

guessability_tips = """

Security Warning: Password rejected due to being weak and predictable.

NIST-aligned guidance:

- Use a long passphrase (12+ characters is better than short complexity)
- Avoid personal info (names, birthdays, years) and common patterns
- Use unique passwords for each account
- Mix upper/lowercase letters, numbers, and symbols
- Avoid repeated characters or sequences.
- Consider using a password manager (e.g lastpass) to generate strong passwords

Try again with a stronger password.

"""


if __name__ == "__main__":
    print(" A Standalone Password Risk Assessment Tool Using Breach Intelligence and Guessability Modelling  ")

    #Storing the user passowrd input 
    user_password = getpass.getpass("Please enter a password:\n" )

    if user_password in leaked_password:
        print("Status: NON ACCEPTABLE (Password has been breached in Local Database) \n")
        print(warning_message)
    else: 
        try: 
            pass_online = online_check(user_password)
        except Exception:
            pass_online = None 
    
        if pass_online is None:
            print ("Online check is unavailable\n")
            status, guesses, reasons = guessability.decision(user_password)

            if status == "NON ACCEPTABLE":
                print("Password in NON ACCEPTABLE, Please input a different password to run a different check\n")
                print("Estimated guesses:", guesses)
                for r in reasons:
                    print ("-", r)
                print(guessability_tips)
            else:
                print("Password in ACCEPTABLE\n")
                print("Estimated guesses:\n", guesses)

        elif pass_online > 0 :
            print("Status: NON ACCEPTABLE (Password has been breached in Online Database) \n")
            print("Found " + str(pass_online) + " times")
            print(warning_message)

        else:
            status, guesses, reasons = guessability.decision(user_password)
            if status == "NON ACCEPTABLE":
                print("Password in NON ACCEPTABLE, Please input a different password to run a dfifrent check\n")
                print("Estimated guesses:", guesses)
                for r in reasons:
                    print ("-", r)
                print(guessability_tips)
            else:
                print("Password in ACCEPTABLE\n")
                print("Estimated guesses:", guesses)
