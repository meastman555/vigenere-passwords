#program that encrypts and decrypts passwords using a user-remembered key and the Vigenere Cypher
from os import path
from string import ascii_lowercase as alpha
from fileops import add_info, get_password, get_contents, write_info, sort_file

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
    account = input(f"Encrypted password is {encrypted_password}. What account is this for? ")
    #write account-salted pair to the file specifiec
    add_info(file_name, account.upper(), encrypted_password)
    sort_file(file_name)
    print("Password successfully encrypted")

#don't have to sort it because file line relative order is preserved
#if the account specified doesn't have an entry, this method does nothing
def delete(file_name):
    del_account = input("What is the name of the account you want to delete? ").upper()
    #reads all of file's contents into list
    file_lines = get_contents(file_name)
    #goes through each line in file and 
    for line in file_lines:
        account, password = line.strip().split("-")
        #if the account is the delete account, delete the entire line from the list of file lines
        if account == del_account:
            file_lines.remove(line)
    #rewrite all the remaining lines
    write_info(file_name, file_lines)

#updates the account's, password (with or without same key), or key
def update(file_name):
    pass


#prints the valid operations
def print_operations():
    print("\n---- Available operations ----")
    print("> \"encrypt\" -- links an encrypted password to an account using a user-specified key")
    print("> \"decrypt\" -- decrypts a stored password after given a user-specified account and key")
    print("> \"delete\" -- deletes a user-specified account from the file")
    print("> \"update\" -- updates the password for a user-specified account")
    print("> \"list\" -- alphabetically lists all accounts current in the file")
    print("> \"quit\" -- exits the program\n")

#prints the starting program info
def print_starting_info():
    print("This is a basic password encryption/decryption program that uses the vigenere cipher.")
    print("The cipher uses a memorized key that is used in encryption and decryption.")

#"main" portion of code
if __name__ == "__main__":
    print_starting_info()
    file_name = input("What is the name of the storage file? (if not in the same directory as this file, please provide the entire filepath): ")
    print_operations()
    #checks to make sure the file given exists
    if not path.exists(file_name):
        print("File not found. Aborting program")
        quit()
    #main loop of program
    while True:
        operation = input("Please type the operation you wish to perform, or \"help\" to see them listed: ").lower()
        if operation == "decrypt":
            decrypt(file_name)
        elif operation == "encrypt":
            encrypt(file_name)
        elif operation == "delete":
            delete(file_name)
        elif operation == "update":
            update(file_name)
        elif operation == "help":
            print_operations()
        elif operation == "quit":
            print("Quitting program...")
            break
