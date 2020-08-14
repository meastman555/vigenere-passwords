#program that encrypts and decrypts passwords using a user-remembered key and the Vigenere Cypher
from os import path
from string import ascii_lowercase as alpha
from fileops import add_info, get_password, get_contents, write_info, write_blank

def decrypt(file_name):
    account = input("What account is the password for? ")
    #gets associated password from this account, if one exists
    encrypted_password = get_password(file_name, account.upper());
    if encrypted_password == None:
        print("No encrypted password for this account exists")
    else:
        key = input("What is the key that will be used to decrypt? ")
        plain_text = ""
        key_index = 0
        #reverses the algorithm for encryption by subtracting char values, no wrapping needed
        #only uses algorithm for alphabetic characters
        for curr_char in encrypted_password.strip("\n"):
            if 97 <= ord(curr_char.lower()) <= 122:
                old_char = alpha[alpha.index(curr_char.lower()) - alpha.index(key[key_index])]
                #makes the original char lowercase if the encrypted one was
                old_char = old_char.upper() if curr_char.isupper() else old_char
            #digits and special charactes just get added on
            else:
                old_char = curr_char
            plain_text += old_char
            #wraps the key index the same way as encryption
            key_index = (key_index + 1) % len(key)
        print(f"The decrypted password is \"{plain_text}\"")

def encrypt(file_name):
    plain_text = input("What is the password you wish to encrypt? ")
    key = input("What is the key that will be used to encrypt? ").lower()
    encrypted_password = ""
    key_index = 0
    for curr_char in plain_text:
        #if the character is alphabetic (lower or upper)
        if 97 <= ord(curr_char.lower()) <= 122:
            #adds the key's current alpha value to current plain text's alpha value, wraps if necessary
            new_char = alpha[(alpha.index(key[key_index]) + alpha.index(curr_char.lower())) % 26]
            #makes the new char uppercase if the original one was
            new_char = new_char.upper() if curr_char.isupper() else new_char
        #special characters and numbers just get added on
        else:
            new_char = curr_char
        encrypted_password += new_char
        #wraps key index if necessary
        key_index = (key_index + 1) % len(key)
    account = input(f"Encrypted password is {encrypted_password}. What account is this for? (If multiple accounts, separate with commas): ")
    #write account-salted pair to the file specifiec
    add_info(file_name, account.upper(), encrypted_password)
    print("Password successfully encrypted")

#deletes the account and password for the account specified
#if the account's password has multiple accounts tied to it, only removes this account
#if there are no accounts in file or no password for specified account, this method does nothing
def delete(file_name):
    del_account = input("What is the name of the account you want to delete? ").upper()
    #reads all of file's contents into list
    file_lines = get_contents(file_name)
    #goes through each line in file
    for line in file_lines:
        account_string, password = line.split("-")
        accounts = account_string.split(",")
        #splits line into accounts and passwords, then loops through each account (if multiple)
        for curr_account in accounts:
            if curr_account == del_account:
                accounts.remove(curr_account)
        #if there were multiple accounts for this password file still shows the other ones
        if len(accounts) > 0:
            write_info(file_name, accounts, password)
        #"writes" over the line on the file by replacing it with an empty string
        else:
            write_blank(file_name)

#updates the account/s, password (with or without same key), or key
def update(file_name):
    pass

#"main" portion of code
if __name__ == "__main__":
    file_name = input("What is the name of the storage file? ")
    #checks to make sure the file given exists
    if not path.exists(file_name):
        print("File not found. Aborting program")
        quit()

    #main loop of program
    while True:
        operation = input("Do you wish to encrypt, decrypt, delete an account, update info for an account (CURRENTLY NOT IMPLEMENTED), or quit the program? ").lower()
        if operation == "decrypt":
            decrypt(file_name)
        elif operation == "encrypt":
            encrypt(file_name)
        elif operation == "delete":
            delete(file_name)
        elif operation == "update":
            update(file_name)
        elif operation == "quit":
            print("Quitting program...")
            break
