# import modules
import mysql.connector as sql
from random import randint

# Establishment of connection to mysql server
print("Enter the details of your MYSQL Server:")
x = input("Hostname: ")
y = input("User: ")
z = input("Password: ")

con = sql.connect(
    host=x,
    user=y,
    password=z
)
con.autocommit = True
cur = con.cursor()

# creation of Database and subsequent Tables
cur.execute("CREATE DATABASE IF NOT EXISTS TRAIN_DETAILS;")
cur.execute("USE TRAIN_DETAILS;")
s = """
CREATE TABLE IF NOT EXISTS DETAILS(
    id INT PRIMARY KEY,
    passenger VARCHAR(16),  -- password
    name VARCHAR(70),
    gender CHAR(1),
    age VARCHAR(3),
    dob DATE,
    phone_No CHAR(10)
);
"""
cur.execute(s)

s = """
CREATE TABLE IF NOT EXISTS TICKETS(
    id INT,
    PNR INT,
    train VARCHAR(25),
    Doj DATE,
    tfr VARCHAR(100),
    tto VARCHAR(100)
);
"""
cur.execute(s)


# login menu
def login_menu():
    print("WELCOME TO THE IRCTC PORTAL")
    print("1. Create New Account")
    print("2. Log In")
    print("3. Exit")
    opt = int(input("Enter your choice: "))
    if opt == 1:
        create_acc()
    elif opt == 2:
        login()
    else:
        e = input("Exit the portal? (Y/N): ")
        if e in "Nn":
            login_menu()


# Account creation
def create_acc():
    print("Enter the details to create your account:")
    i = randint(1000, 10000)
    print(f"Your generated ID is: {i}")
    p = input("Enter your password: ")
    n = input("Enter your name: ")
    gender = input("Enter your gender (M/F/O): ")
    age = input("Enter your age: ")
    dob = input("Enter your date of birth (YYYY-MM-DD): ")
    ph = input("Enter your contact number: ")

    s1 = (
        "INSERT INTO DETAILS (id, passenger, name, gender, age, dob, phone_No) "
        f"VALUES ({i}, '{p}', '{n}', '{gender.upper()}', '{age}', '{dob}', '{ph}');"
    )

    cur.execute(s1)
    print("Now you may login with your newly created account!")
    login()


# login to account
def login():
    global a
    try:
        a = int(input("Enter your ID: "))
        b = input("Enter your password: ")
        s2 = (
            "SELECT name FROM DETAILS "
            f"WHERE id = {a} AND passenger = '{b}';"
        )
        cur.execute(s2)
        j = cur.fetchone()
        if j is None:
            raise ValueError("No such user")

        print(f"Welcome back {j[0]}!")
        main_menu()
    except Exception as e:
        print("Your account was not found!", e)
        print("You can: \n"
              "1. Try logging in again \n"
              "2. Create a new account")
        ch = input("Enter your choice: ")
        if ch == '1':
            login()
        elif ch == '2':
            create_acc()
        else:
            print("Invalid choice!")
            x1 = input("Exit the portal? (Y/N): ")
            if x1 in "Nn":
                login_menu()

# main menu
def main_menu():
    print("What would you like to do today? \n"
          "1. Purchase a Ticket \n"
          "2. Check Ticket Status / Cancel Ticket \n"
          "3. Request a refund (Cancel Ticket) \n"
          "4. Account Settings \n"
          "5. Logout \n"
          "6. Exit")
    ch1 = int(input("Enter your choice: "))
    if ch1 == 1:
        buy_ticket()
    elif ch1 == 2 or ch1 == 3:
        show_ticket()
    elif ch1 == 4:
        account()
    elif ch1 == 5:
        login_menu()
    else:
        exit_program()


# exit_prompt
def exit_program():
    x2 = input("Would you like to exit (Y/N)? ")
    if x2.upper() == "N":
        main_menu()


# back to main_menu
def back_to_main_menu():
    x3 = input("Return to the main menu (Y/N)? ")
    if x3.upper() == 'Y':
        print("Returning to the Main menu...")
        main_menu()


# ticket creation
def buy_ticket():
    print("Enter details of your journey: ")
    i = a
    pnr = randint(100000, 1000000)
    print(f"Your PNR is {pnr}")
    train = input("Enter the name of train: ")
    doj = input("Enter the date of journey (YYYY-MM-DD): ")
    fr = input("Enter the Departing station: ")
    to = input("Enter the Destination station: ")

    s4 = (
        "INSERT INTO TICKETS (id, PNR, train, Doj, tfr, tto) "
        f"VALUES ({i}, {pnr}, '{train}', '{doj}', '{fr}', '{to}');"
    )
    cur.execute(s4)
    back_to_main_menu()


# ticket checking / cancelling
def show_ticket():
    try:
        pnr = int(input("Enter your PNR: "))
        s5 = f"SELECT * FROM TICKETS WHERE PNR = {pnr};"
        cur.execute(s5)
        j = cur.fetchone()
        if j is None:
            raise ValueError("No such ticket")

        if j[0] == a:
            print(f"PNR: {j[1]} \n"
                  f"Train: {j[2]} \n"
                  f"Date of Journey: {j[3]} \n"
                  f"From: {j[4]} \n"
                  f"To: {j[5]}")
            x4 = input("Do you really want to cancel this ticket (Y/N)? ")
            if x4.upper() == 'Y':
                s3 = f"DELETE FROM TICKETS WHERE PNR = {pnr};"
                cur.execute(s3)
                print("You will be refunded shortly.")
                back_to_main_menu()
            else:
                back_to_main_menu()
        else:
            print("Unauthorized! \n"
                  "Your ID does not match the PNR of ticket.")
            back_to_main_menu()
    except Exception as e:
        print("Error:", e)
        ticket_not_found()


# if ticket is not found
def ticket_not_found():
    print("Ticket not found!")
    print("You can: \n"
          "1. Try entering your PNR number again \n"
          "2. Purchase a ticket \n"
          "3. Return to Main Menu \n"
          "4. Exit")
    ch = int(input("Enter your choice: "))
    if ch == 1:
        show_ticket()
    elif ch == 2:
        buy_ticket()
    elif ch == 3:
        print("Returning to main menu...")
        main_menu()
    else:
        exit_program()
# Account settings
def account():
    print("Do you want to :\n"
          "1. Show Account details \n"
          "2. Delete Account")
    ch = int(input("Enter your choice: "))
    if ch == 1:
        s4 = f"SELECT * FROM DETAILS WHERE id = {a};"
        cur.execute(s4)
        j = cur.fetchone()
        if j:
            print(f"ID: {j[0]} \n"
                  f"Password: {j[1]} \n"
                  f"Name: {j[2]} \n"
                  f"Gender: {j[3]} \n"
                  f"Age: {j[4]} \n"
                  f"DOB: {j[5]} \n"
                  f"Phone Number: {j[6]}")
        else:
            print("Account not found.")
        back_to_main_menu()
    elif ch == 2:
        x6 = input("Do you want to request refund for your ticket(s) too? (Y/N) ")
        if x6.upper() == "Y":
            s5 = f"DELETE FROM TICKETS WHERE id = {a};"
            cur.execute(s5)
            print("You will be refunded shortly!")
        s6 = f"DELETE FROM DETAILS WHERE id = {a};"
        cur.execute(s6)
        print("Account Successfully Deleted!")
        login_menu()
    else:
        back_to_main_menu()
# Calling the first function, hence starting the program
if __name__ == "__main__":
    login_menu()
