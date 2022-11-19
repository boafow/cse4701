from DBInterface import dbinterface

if __name__ == "__main__":
    print("Welcome to the company database!")
    user = input("Enter user: ")
    password = input("Enter password: ")
    
    db = dbinterface("localhost", user, password, "companydb")
    choice = 69
    
    while choice != 0:
        db.print_menu()

        choice = int(input("Enter choice: "))
        if choice == 1:
            db.create_new_employee()
        elif choice == 2:
            ssn = input("Enter ssn: ")
            db.view_employee(ssn)
        elif choice == 3:
            ssn = input("Enter ssn: ")
            db.modify_employee(ssn)
        elif choice == 4:
            db.remove_employee()
        elif choice == 5:
            db.add_new_dependent()
        elif choice == 6:
            db.remove_dependent()
        elif choice == 7:
            db.add_new_department()
        elif choice == 8:
            db.view_department()
        elif choice == 9:
            dnumber = input("Enter department number: ")
            db.remove_department(dnumber)
        elif choice == 10:
            db.add_department_location()
        elif choice == 11:
            db.remove_department_location()
        elif choice == 0:
            db.close()
            break
    