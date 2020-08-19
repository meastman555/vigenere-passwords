#file will only save the encrypted passwords/token
#key must be remembered by the user

#loops through the file until finding an entry that matches account, then return its encrypted password
#if cannot find entry in file, returns NONE
def get_password(file_name, account):    
    with open(file_name) as f:
        for line in f:
            account_string, encrypted_password = line.split("-")
            if account_string.strip() == account:
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
def write_info(file_name, lines):
    with open(file_name, "w") as f:
        f.writelines(lines)

#sorts the contents of the file alphabetically
#called at the end of the methods that add new entries to the file
def sort_file(file_name):
    with open(file_name, "r") as f:
        lines = f.readlines();
        sorted_lines = sorted(lines)
    with open(file_name, "w") as f:
        f.writelines(sorted_lines)

#checks to see whether the account passed already has an entry in the account
#returns true if already present, false if missing
def account_present(file_name, account):
    with open(file_name, "r") as f:
        lines = f.readlines()
        for line in lines:
            curr_account, password = line.split("-")
            if curr_account == account:
                return True
        return False

