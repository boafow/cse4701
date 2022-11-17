from DBInterface import dbinterface

if __name__ == "__main__":
    #ask for user input for host, user, password, database
   
    
    print("Welcome to the company database!")
    host = input("Enter host: ")
    user = input("Enter user: ")
    password = input("Enter password: ")
    database = input("Enter database: ")
    
    db = dbinterface(host, user, password, database)
    db.print_menu()
    choice = int(input("Enter choice: "))
    
    
    