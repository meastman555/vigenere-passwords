#file will only save the encrypted passwords/token
#key must be remembered by the user

#loops through the file until finding an entry that matches account, then return its encrypted password
#if cannot find entry in file, returns NONE
def get_password(file_name, account):    
    with open(file_name) as f:
        for line in f:
            account_string, encrypted_password = line.split("-")
            list_of_accounts = account_string.split(",")
            for curr_account in list_of_accounts:
                if curr_account.strip() == account:
                    return encrypted_password    

#writes the account name and encrypted password to the file
def add_info(file_name, account, encrypted_password):
    #if user gives nonexistent file to encrypt to, file will be created
    with open(file_name, "a+") as f:
        line = account + "-" + encrypted_password
        f.write(line+"\n")

#returns the contents of the file as a list of strings
def get_contents(file_name):
    with open(file_name, "r") as f:
        return f.readlines();

#writes the contents passed to the file instead of appending
def write_info(file_name, accounts, encrypted_password):
    with open(file_name, "w") as f:
        #if multiple accounts, join them with a comma
        f.write(",".join(accounts) + "-" + encrypted_password + "\n")

#to "delete" an account, actually just write an empty string
#only important if account deleted is the only account
def write_blank(file_name):
    with open(file_name, "w") as f:
        f.write("")
