import mysql.connector
from mysql.connector import errorcode

class dbinterface:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
    
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
        
        
    def create_new_employee(self, fname, minit, lname, ssn, bdate, address, sex, salary, superssn, dno):
        mycursor = self.mydb.cursor()
        sql = "SELECT * FROM employees WHERE ssn = %s FOR SHARE"
        
        
        sql = "INSERT INTO employees (fname, minit, lname, ssn, bdate, address, sex, salary, superssn, dno) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (fname, minit, lname, ssn, bdate, address, sex, salary, superssn, dno)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        self.mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        
    def view_employee(self, ssn):
        mycursor = self.mydb.cursor()
        sql = "SELECT * FROM employees WHERE ssn = %s"
        val = (ssn,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
            
    def modify_employee(self, id, name, age, salary):
        mycursor = self.mydb.cursor()
        sql = "UPDATE employees SET name = %s, age = %s, salary = %s WHERE id = %s"
        val = (name, age, salary, id)
        mycursor.execute(sql, val)
        self.mydb.commit()
        print(mycursor.rowcount, "record(s) affected")
        
    def remove_employee(self, id):
        mycursor = self.mydb.cursor()
        sql = "DELETE FROM employees WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        self.mydb.commit()
        print(mycursor.rowcount, "record(s) deleted")
        
    def add_new_dependent(self, name, age, relation, employee_id):
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO dependents (name, age, relation, employee_id) VALUES (%s, %s, %s, %s)"
        val = (name, age, relation, employee_id)
        mycursor.execute(sql, val)
        self.mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        
    def remove_dependent(self, id):
        mycursor = self.mydb.cursor()
        sql = "DELETE FROM dependents WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        self.mydb.commit()
        print(mycursor.rowcount, "record(s) deleted")
        
    def add_new_department(self, name):
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO departments (name) VALUES (%s)"
        val = (name,)
        mycursor.execute(sql, val)
        self.mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        
    def view_department(self, id):
        mycursor = self.mydb.cursor()
        sql = "SELECT * FROM departments WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
            
    def remove_department(self, id):
        mycursor = self.mydb.cursor()
        sql = "DELETE FROM departments WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        self.mydb.commit()
        print(mycursor.rowcount, "record(s) deleted")
        
    def view_department(self, id):
        mycursor = self.mydb.cursor()
        sql = "SELECT * FROM departments WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x)
            
    def add_department_location(self, department_id, location):
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO department_locations (department_id, location) VALUES (%s, %s)"
        val = (department_id, location)
        mycursor.execute(sql, val)
        self.mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        
    def remove_department_location(self, id):
        mycursor = self.mydb.cursor()
        sql = "DELETE FROM department_locations WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        self.mydb.commit()
        print(mycursor.rowcount, "record(s) deleted")