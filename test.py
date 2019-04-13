# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 16:05:02 2018

@author: kevin he
"""
from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector

mydb=mysql.connector.connect(
    host="localhost",
    user='root',
    passwd='hejia123',
    database='stocks'
        )
mycursor = mydb.cursor()

tomorrow = datetime.now().date() + timedelta(days=1)

create_sql="CREATE TABLE employees (first_name VARCHAR(255), last_name VARCHAR(255), hire_date datetime, gender VARCHAR(255), birth_date datetime)"

mycursor.execute(create_sql)

add_employee = ("INSERT INTO employees "
               "(first_name, last_name, hire_date, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")
add_salary = ("INSERT INTO salaries "
              "(emp_no, salary, from_date, to_date) "
              "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")

data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

# Insert new employee
mycursor.execute(add_employee, data_employee)


# Insert salary information



# Make sure data is committed to the database
mydb.commit()

mycursor.close()
mydb.close()
