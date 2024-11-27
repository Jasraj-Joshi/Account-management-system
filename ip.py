# import area 
import pandas as pd
import mysql.connector
from datetime import datetime
import os

# MySQL connection
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "account_management"
}

# Establish connection
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit()

# Create a DataFrame to manage accounts in memory
account_data = pd.DataFrame(columns=["Account ID", "Name", "Email", "Balance"])

# def area

# Add a user to the system
def add_user(username, password):
    """Adds a new user to the users table."""
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()
        print(f"User {username} created successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Create a dynamic table for each user (user-specific accounts and transactions)
def create_user_tables(user_id):
    """Creates unique account and transaction tables for a user."""
    try:
        # Create user-specific account table
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS user_{user_id}_accounts (
            account_id INT AUTO_INCREMENT PRIMARY KEY,
            account_holder_name VARCHAR(255),
            email VARCHAR(255),
            balance FLOAT DEFAULT 0.0
        );
        """)
        
        # Create user-specific transactions table
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS user_{user_id}_transactions (
            transaction_id INT AUTO_INCREMENT PRIMARY KEY,
            account_id INT,
            transaction_type VARCHAR(10),
            amount FLOAT,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES user_{user_id}_accounts(account_id)
        );
        """)
        conn.commit()
        print(f"Tables for user {user_id} created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to authenticate user based on password
def authenticate_user(username, password):
    """Checks if username and password are correct."""
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            print(f"Login successful for user: {username}")
            return user[0]  # Return user ID
        else:
            print("Incorrect username or password.")
            return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Add a new account for the logged-in user
def add_account(user_id, name, email, initial_balance=0.0):
    """Adds a new account for the logged-in user."""
    try:
        cursor.execute(
            f"INSERT INTO user_{user_id}_accounts (account_holder_name, email, balance) VALUES (%s, %s, %s)",
            (name, email, initial_balance)
        )
        conn.commit()
        account_id = cursor.lastrowid
        print(f"Account created successfully for {name}! Account ID: {account_id}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Record a transaction for the logged-in user
def record_transaction(user_id, account_id, transaction_type, amount):
    """Records a transaction and updates balance for the logged-in user."""
    try:
        cursor.execute(f"SELECT balance FROM user_{user_id}_accounts WHERE account_id = %s", (account_id,))
        result = cursor.fetchone()
        if not result:
            print("Account not found.")
            return
        
        current_balance = result[0]
        new_balance = current_balance + amount if transaction_type == "DEPOSIT" else current_balance - amount
        
        if new_balance < 0:
            print("Insufficient balance.")
            return
        
        cursor.execute(
            f"UPDATE user_{user_id}_accounts SET balance = %s WHERE account_id = %s", (new_balance, account_id)
        )
        cursor.execute(
            f"INSERT INTO user_{user_id}_transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
            (account_id, transaction_type, amount)
        )
        conn.commit()
        print(f"{transaction_type} of {amount} successful! New Balance: {new_balance}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# View account details for the logged-in user
def view_account(user_id, account_id):
    """Displays account details for the logged-in user."""
    try:
        cursor.execute(f"SELECT * FROM user_{user_id}_accounts WHERE account_id = %s", (account_id,))
        account = cursor.fetchone()
        if account:
            print(f"Account Details:\nID: {account[0]}\nName: {account[1]}\nEmail: {account[2]}\nBalance: {account[3]}")
        else:
            print("Account not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# View transaction history for the logged-in user
def transaction_history(user_id, account_id):
    """Displays transaction history for the logged-in user."""
    try:
        cursor.execute(f"SELECT * FROM user_{user_id}_transactions WHERE account_id = %s", (account_id,))
        transactions = cursor.fetchall()
        if transactions:
            history = pd.DataFrame(
                transactions,
                columns=["Transaction ID", "Account ID", "Type", "Amount", "Date"],
            )
            print("Transaction History:")
            print(history)
        else:
            print("No transactions found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to clear screen
def clear_screen():
    """Clears the screen after each operation."""
    os.system('cls')

# Menu for logged-in user
def main():
    print("Welcome to Account Management System!")
    
    # User login
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    user_id = authenticate_user(username, password)
    
    if user_id:
        # Create user-specific tables if not already created
        create_user_tables(user_id)
        
        while True:
            print(
                """
+-------+---------------------------------+
|Sr No. |     Account Management          |
+-------+---------------------------------+
|     1.|   Add Account                   |
|     2.|   Deposit                       |
|     3.|   Withdrawl                     |
|     4.|   View Account                  |
|     5.|   Transaction History           |
|     6.|   Exit                          |
+-------+---------------------------------+       
            """
            )
            choice = input("Enter your choice \n >>>")
            
            if choice == "1":
                name = input("Enter account holder name: ")
                email = input("Enter email: ")
                initial_balance = float(input("Enter initial balance: "))
                add_account(user_id, name, email, initial_balance)
                clear_screen()  # Clear screen after performing task
            elif choice == "2":
                account_id = int(input("Enter account ID: "))
                amount = float(input("Enter deposit amount: "))
                record_transaction(user_id, account_id, "DEPOSIT", amount)
                clear_screen()  # Clear screen after performing task
            elif choice == "3":
                account_id = int(input("Enter account ID: "))
                amount = float(input("Enter withdrawal amount: "))
                record_transaction(user_id, account_id, "WITHDRAW", -amount)
                clear_screen()  # Clear screen after performing task
            elif choice == "4":
                account_id = int(input("Enter account ID: "))
                view_account(user_id, account_id)
                clear_screen()  # Clear screen after performing task
            elif choice == "5":
                account_id = int(input("Enter account ID: "))
                transaction_history(user_id, account_id)
                clear_screen()  # Clear screen after performing task
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                clear_screen()  # Clear screen after invalid input

# Run the program
if __name__ == "__main__":
    main()

# Close connection
cursor.close()
conn.close()
# the code ends here 