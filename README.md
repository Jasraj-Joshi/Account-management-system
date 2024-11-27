# Account-management-system

this is a python program to manage account this worls like it takes user info and store in sql data base 
here are some imp sql commands to do so 

CREATE DATABASE IF NOT EXISTS account_management;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_<user_id>_accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    account_holder_name VARCHAR(255),
    email VARCHAR(255),
    balance FLOAT DEFAULT 0.0
);
here user id will be changed to specific name

CREATE TABLE IF NOT EXISTS user_<user_id>_transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    transaction_type VARCHAR(10),
    amount FLOAT,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES user_<user_id>_accounts(account_id)
);

use this in sql for perfect use of this project
