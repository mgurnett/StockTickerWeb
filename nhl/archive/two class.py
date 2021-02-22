class Employee: 

    # constructor for initillization 
    def __init__(self, name, age): 
        self.name = name 
        self.age = age 

    # instance method 
    def emp_data(self): 
        print('Name of Employee : ', self.name) 
        print('Age of Employee : ', self.age) 


class Data: 
    def __init__(self, address, salary, emp_obj): 
        self.address = address 
        self.salary = salary 

        # creating object of Employee class 
        self.emp_obj = emp_obj 

    # instance method 
    def display(self): 

        # calling Employee class emp_data() 
        # method 
        self.emp_obj.emp_data() 
        print('Address of Employee : ', self.address) 
        print('Salary of Employee : ', self.salary) 

# creating Employee class object 
emp = Employee('Ronil', 20) 

# passing obj. of Emp. class during creation 
# of Data class object 
data = Data('Indore', 25000, emp) 

# call Data class instance method 
data.display()
================================

class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age
person_list = [Person("Amy", 25), Person("Bob", 30), Person("Cat", 25)]

age_25_list = [p for p in person_list if p.age == 25]

for person in age_25_list:
    print(person.name)
OUTPUT
Amy
Cat
