import mysql.connector as mq
myInfo = mq.connect(
        host="localhost",
        port="6925",
        user="root",
        password="Tolulope1",
        database="bankingSystem_db",
        auth_plugin='mysql_native_password'
)
myCursor = myInfo.cursor()
# myCursor.execute("CREATE DATABASE bankingSystem_db")
# myCursor.execute('''
#   CREATE TABLE accounts (
#           account_number VARCHAR(10) PRIMARY KEY,
#           account_holder_name VARCHAR(100),
#           balance DECIMAL(10, 2),
#           date_of_creation DATE,
#           Email VARCHAR (100),
#           PhoneNumber VARCHAR (20),
#           Address VARCHAR (100),
#           Password VARCHAR (50),
#           locked_amount DECIMAL(10, 2) DEFAULT 0
# )
# ''')


# myCursor.execute('''
#  CREATE TABLE recharge_cards (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     amount DECIMAL(10, 2),
#     PhoneNumber VARCHAR (20),
#     FOREIGN KEY (PhoneNumber) REFERENCES accounts(PhoneNumber)
# ); 
# ''')
# myCursor.execute('''  
#  CREATE TABLE loans (
#     loan_id INT AUTO_INCREMENT PRIMARY KEY,
#     account_number VARCHAR(100),
#     amount DECIMAL(10, 2),
#     status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
#     FOREIGN KEY (account_number) REFERENCES accounts(account_number)
# )
# ''')