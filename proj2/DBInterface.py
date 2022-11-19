import mysql.connector
from mysql.connector import errorcode


class dbinterface:
    def __init__(self, host, user, password, database):
        
        self.mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    
    def close(self):
        self.mydb.close()
        print("Connection closed")
    
    def print_menu(self):
        print("1. Create new employee")
        print("2. View employee")
        print("3. Modify employee")
        print("4. Remove employee")
        print("5. Add new dependent")
        print("6. Remove dependent")
        print("7. Add new department")
        print("8. View department")
        print("9. Remove department")
        print("10. Add department location")
        print("11. Remove department location")
        print("0. Exit")
        
    def create_new_employee(self):
        try:    

            fname = input("Enter first name: ")
            minit = input("Enter middle initial: ")
            lname = input("Enter last name: ")
            ssn = input("Enter ssn: ")
            bdate = input("Enter birth date: ")
            address = input("Enter address: ")
            sex = input("Enter sex; M or F: ")
            salary = input("Enter salary: ")
            superssn = input("Enter supervisor ssn: ")
            dno = input("Enter department number: ")
            
            if superssn == "":
                superssn = None
        
            mycursor = self.mydb.cursor()
            sql = "INSERT INTO EMPLOYEE (Fname, Minit, Lname, Ssn, Bdate, Address, Sex, Salary, Super_ssn, Dno) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (fname, minit, lname, ssn, bdate, address, sex, salary, superssn, dno)
            mycursor.execute(sql, val)
            self.mydb.commit()
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
                
        except mysql.connector.errors.IntegrityError:
            print("Cannot add employee. There is a constraint violation. Try again.")
            self.create_new_employee()
        except mysql.connector.errors.DataError:
            print("Cannot add employee. There is a data error. Try again.")
            self.create_new_employee()
        except mysql.connector.errors.DatabaseError:
            print("Cannot add employee. An invalid input was entered for a field. Try again.")
            self.create_new_employee()
        
    #will not show employees that are managers of the same department as another employee
    def view_employee(self, ssn):
        mycursor = self.mydb.cursor()
        sql = "SELECT e.Fname, e.Minit, e.Lname, e.Salary, e.Super_ssn, e.Dno, d.Dname, d.Mgr_ssn, d.Mgr_start_date, de.Dependent_name FROM EMPLOYEE e JOIN DEPARTMENT d ON e.Dno = d.Dnumber JOIN DEPENDENT de ON e.Ssn = de.Essn WHERE e.Ssn = %s"
        val = (ssn,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            sql = "SELECT e.Fname, e.Minit, e.Lname, e.Salary, e.Super_ssn, e.Dno, d.Dname, d.Mgr_ssn, d.Mgr_start_date FROM EMPLOYEE e JOIN DEPARTMENT d ON e.Dno = d.Dnumber WHERE e.Ssn = %s"
            val = (ssn,)
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()  
        for x in myresult:
            print(x)
    
    def modify_employee(self, ssn):
        try:
            mycursor = self.mydb.cursor()
            lock = "SELECT * FROM EMPLOYEE WHERE Ssn = %s FOR SHARE"
            lockval = (ssn,)
            mycursor.execute(lock, lockval)
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
                
            selection = input("Enter the field you would like to modify (address, sex, salary, super_ssn, Dno): ").lower()
            if selection == "address":
                newval = input("Enter new address: ")
            elif selection == "sex":
                newval = input("Enter new sex: ")
            elif selection == "salary":
                newval = input("Enter new salary: ")
            elif selection == "super_ssn":
                newval = input("Enter new super_ssn: ")
            elif selection == "dno":
                newval = input("Enter new dno: ")
            else:
                print("Invalid input. Try again.")
                self.modify_employee(ssn)
            
            sql = "UPDATE EMPLOYEE SET " + selection[0:1].upper()+selection[1:] + " = %s WHERE Ssn = %s"
            val = (newval, ssn)
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            self.mydb.commit()
            for x in myresult:
                print(x)
            
            continue_updating = input("Would you like to update another field? (y/n): ").lower()
            if continue_updating == "y":
                self.modify_employee(ssn)
            elif continue_updating == "n":
                return
        except mysql.connector.errors.InternalError:
            print("the database is locked. Finish other instance of the program and try again.")
            return
         
    def remove_employee(self):
        try:
            mycursor = self.mydb.cursor()
            ssn = input("Enter the ssn of the employee you would like to remove: ")
            lock = "SELECT * FROM EMPLOYEE WHERE Ssn = %s FOR SHARE"
            lockval = (ssn,)
            mycursor.execute(lock, lockval)
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
            
            confirmation = input("Are you sure you want to remove this employee? (y/n): ").lower()
            if confirmation == "y":
                sql = "DELETE FROM EMPLOYEE WHERE Ssn = %s"
                val = (ssn,)
                mycursor.execute(sql, val)
                self.mydb.commit()
                for x in myresult:
                    print(x)
            elif confirmation == "n":
                return
            else:
                print("Invalid input. Try again.")
        except mysql.connector.errors.IntegrityError:
            print("Cannot remove employee. Dependencies exist, please remove dependencies first.")
        except mysql.connector.errors.InternalError:
            print("the database is locked. Finish other instance of the program and try again.")
            return
            
    def add_new_dependent(self):
        try:
            mycursor = self.mydb.cursor()
            ssn = input("Enter the ssn of the employee you would like to add a dependent to: ")
            lock = "SELECT e.Fname, e.Minit, e.Lname, de.Dependent_name FROM EMPLOYEE e JOIN DEPENDENT de ON e.Ssn = de.Essn WHERE e.Ssn = %s FOR SHARE"
            lockval = (ssn,)
            mycursor.execute(lock, lockval)
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
            
            print("Enter the following information for the new dependent.")
            dependent_name = input("Enter dependent name: ")
            sex = input("Enter sex: ")
            bdate = input("Enter birth date: ")
            relationship = input("Enter relationship: ")
            
            sql = "INSERT INTO DEPENDENT (Essn, Dependent_name, Sex, Bdate, Relationship) VALUES (%s, %s, %s, %s, %s)"
            val = (ssn, dependent_name, sex, bdate, relationship)
            mycursor.execute(sql, val)
            self.mydb.commit()
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
        except mysql.connector.errors.IntegrityError:
            print("Cannot add dependent. There is a constraint violation. Try again.")
            self.add_new_dependent()
        except mysql.connector.errors.DataError:
            print("Cannot add dependent. There is a data error. Try again.")
            self.add_new_dependent()
        except mysql.connector.errors.InternalError:
            print("the database is locked. Finish other instance of the program and try again.")
            return
        
    def remove_dependent(self):
        try:
            mycursor = self.mydb.cursor()
            ssn = input("Enter the ssn of the employee you would like to remove a dependent from: ")
            lock = "SELECT e.Fname, e.Minit, e.Lname, de.Dependent_name FROM EMPLOYEE e JOIN DEPENDENT de ON e.Ssn = de.Essn WHERE e.Ssn = %s FOR SHARE"
            lockval = (ssn,)
            mycursor.execute(lock, lockval)
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
            
            dependent_name = input("Enter the name of the dependent you would like to remove: ")
            sql = "DELETE FROM DEPENDENT WHERE Essn = %s AND Dependent_name = %s"
            val = (ssn, dependent_name)
            mycursor.execute(sql, val)
            self.mydb.commit()
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
        except mysql.connector.errors.IntegrityError:
            print("Cannot remove dependent. There is a constraint violation. Try again.")
            self.remove_dependent()
        except mysql.connector.errors.DataError:
            print("Cannot remove dependent. There is a data error. Try again.")
            self.remove_dependent()
        except mysql.connector.errors.InternalError:
            print("the database is locked. Finish other instance of the program and try again.")
            return
        
    def add_new_department(self):
        #prompt user for input
        try:
            dname = input("Enter department name: ")
            dnumber = input("Enter department number: ")
            mgr_ssn = input("Enter manager ssn: ")
            mgr_start_date = input("Enter manager start date: ")
            
            sql = "INSERT INTO DEPARTMENT (Dname, Dnumber, Mgr_ssn, Mgr_start_date) VALUES (%s, %s, %s, %s)"
            val = (dname, dnumber, mgr_ssn, mgr_start_date)
                    
            mycursor = self.mydb.cursor()
            mycursor.execute(sql, val)

            self.mydb.commit()
                    
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
        except mysql.connector.errors.IntegrityError:
            print("Cannot add department. There is a constraint violation. Try again. Make sure Dnumber is unique.")
            self.add_new_department()
        except mysql.connector.errors.DataError:
            print("Cannot add department. There is a data error. Try again.")
            self.add_new_department()
        
    def view_department(self):
        Dnumber = input("Enter the department number: ")
        mycursor = self.mydb.cursor()
        sql = "SELECT d.Dname, e.Fname, e.Minit, e.Lname, l.Dlocation FROM DEPARTMENT d JOIN EMPLOYEE e ON d.Mgr_ssn = e.Ssn JOIN DEPT_LOCATIONS l ON d.Dnumber = l.Dnumber WHERE d.Dnumber = %s"
        val = (Dnumber,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            print("Could not display department. Please add a department location or check the department number.")
        else:
            for x in myresult:
                print(x)
            
    def remove_department(self, dnumber):
        try:
            mycursor = self.mydb.cursor()
            lock = "SELECT * FROM DEPARTMENT WHERE Dnumber = %s FOR SHARE"
            lockval = (dnumber,)
            mycursor.execute(lock, lockval)
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
                
            sql = "DELETE FROM DEPARTMENT WHERE Dnumber = %s"
            val = (dnumber,)
            mycursor.execute(sql, val)
            self.mydb.commit()
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
            
        except mysql.connector.errors.IntegrityError:
            print("Cannot delete department. Try deleting all dept locations first.")
        except mysql.connector.errors.InternalError:
            print("the database is locked. Finish other instance of the program and try again.")
            return
          
    def add_department_location(self):
        try:
            mycursor = self.mydb.cursor()
            dnumber = input("Enter department number: ")
            lock = "SELECT * FROM DEPT_LOCATIONS WHERE Dnumber = %s FOR SHARE"
            lockval = (dnumber,)
            mycursor.execute(lock, lockval)
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
                
            dlocation = input("Enter department location: ")
            sql = "INSERT INTO DEPT_LOCATIONS (Dnumber, Dlocation) VALUES (%s, %s)"
            val = (dnumber, dlocation)
            mycursor.execute(sql, val)
            self.mydb.commit()
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
        except mysql.connector.errors.IntegrityError:
            print("Cannot add department location. Make sure department exists.")
        except mysql.connector.errors.DataError:
            print("Cannot add department location. There is a data error. Try again.")
            self.add_department_location()
        except mysql.connector.errors.InternalError:
            print("the database is locked. Finish other instance of the program and try again.")
            return

    def remove_department_location(self):
        try:
            mycursor = self.mydb.cursor()
            dnumber = input("Enter department number: ")
            sql = "SELECT * FROM DEPT_LOCATIONS WHERE Dnumber = %s FOR SHARE"
            val = (dnumber,)
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
        
            dlocation = input("Enter department location: ")
            sql = "DELETE FROM DEPT_LOCATIONS WHERE Dnumber = %s AND Dlocation = %s"
            val = (dnumber, dlocation)
            mycursor.execute(sql, val)
            self.mydb.commit()
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x)
        except mysql.connector.errors.DataError:
            print("Cannot remove department location. There is a data error. Try again.")
            self.remove_department_location()
        except mysql.connector.errors.InternalError:
            print("the database is locked. Finish other instance of the program and try again.")
            return