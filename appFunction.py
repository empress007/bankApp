from bankAppDb import myCursor,myInfo
import  random
from datetime import datetime
import re
import sys
from decimal import Decimal

def create_account():
        startWith = "02" 
        number = str(random.randint(10000000, 99999999))
        account_number = startWith+number
        accountHolderName = input("enter your fullname: ").title().strip()
        balance = 0
        date_of_creation = datetime.now().date()
        email = input("Enter your email: ").lower().strip()
        phoneNum = input("Enter your number: ")
        address = input("Please input your address: ").title().strip()
        password = input("Enter password")
      
        
        existingEmail = f"SELECT * FROM accounts WHERE Email = '{email}'"
        myCursor.execute(existingEmail)
        output = myCursor.fetchone()

        if output:
            print('Email already exist, Kindly register with a new email')  
        else:
            existingEmail = f"SELECT * FROM accounts WHERE account_number = '{account_number}'"
            myCursor.execute(existingEmail)
            output = myCursor.fetchone()
            while output:
                print('account taken')
                return account_number 
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            match = re.match(email_pattern, email)
            if not  accountHolderName or not email or not phoneNum or not address :
                print('All fields are required')
            else :
                if match is None:
                    print('enter a valid email')
                else : 
                    values_inputs = "INSERT INTO  accounts (account_number, account_holder_name, balance, date_of_creation, Email, PhoneNumber, Address, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    data = (
                            account_number,accountHolderName,balance,date_of_creation,email,phoneNum,address,password
                        )
                    print("Account Created Successfully")
                    myCursor.execute(values_inputs,data)
                    myInfo.commit()
                   
def login():
   with open('bankApp.txt', 'r') as file:
        lines = file.readlines()
   if lines[0] == "False" :
        email = input("Enter your email: ")
        password = input("Enter your password")
        
   else :
        email = lines[1].strip()
        password = lines[2].strip()
 
   emailQuery = f"SELECT * FROM accounts WHERE Email = '{email}'" 
   myCursor.execute(emailQuery)
   userExist = myCursor.fetchone()

   if userExist:
            if userExist[7] == password:
                print(f''' Welcome {userExist[1]}
                        Press '1' to deposit
                        Press '2' to withdraw
                        Press '3' to apply for loan 
                        Press '4' for recharge card 
                        Press '5' to transfer
                        Press '6' to  lock your cash
                        Press '7' to unlock your cash
                        Press '8' to exit
                    ''')
                f = open("bankApp.txt", 'w')
                f.write(f'True \n{userExist[4]}\n{userExist[7]}')
                f.close()
                choice = input("Choose from the above: ")
                if choice == "1":
                    deposit(userExist[0])
                    
                elif choice == "2":
                    withdraw(userExist)
                    
                elif choice == "3":
                    apply_for_loan(userExist[0])
                    
                elif choice == "4":
                    buy_recharge_card(userExist)
                    
                elif choice == "5":
                    transfer(userExist[0])
                elif choice == "6":
                    lock_money(userExist)
                    
                elif choice == "7":
                    unlock_money(userExist)
                    
                elif choice == "8":
                    f = open("bankApp.txt", 'w')
                    f.write(f'False')
                    f.close()
                    sys.exit('Thanks for banking with us')   
            else:
                print("Incorrect password")
   else:
        print("No user with this information")

                
def deposit(user):
         print('''
               press 1 to deposit
               press 2 to go back 
               ''')
         choice =int(input("choose from the above: "))
         if choice == 1:
            depositAmount = float(input("Enter the amount you want to deposit: "))
            depositQuery = f"UPDATE accounts SET balance = balance + {depositAmount} WHERE account_number = {user}"
            myCursor.execute(depositQuery)
            myInfo.commit()
            print('Deposited successfully')
            login()
         elif choice == 2:
              login() 
         else:
             print("incorrect input")
def withdraw(currentUser):
            print('''
               press 1 to withdraw
               press 2 to go back 
               ''')
            choice =int(input("choose from the above: "))
            if choice == 1:
                withdrawAmount = float(input("how much are you willing to withdraw: "))
                if withdrawAmount <= currentUser[2] :
                    withdrawQuery = f"UPDATE accounts SET balance = balance - {withdrawAmount} WHERE account_number = {currentUser[0]}"
                    myCursor.execute(withdrawQuery)
                    myInfo.commit()
                    currentAmount = currentUser[2] - Decimal(withdrawAmount)
                    print(f"Amount withdrawn successfully \nYour current balance is {currentAmount}")
                    login()
                else:
                 print("Insufficient balance")
            elif choice ==2:
                login() 
            else: 
                print("invalid input") 
def apply_for_loan(currentUser):
        loanAmount = float(input("enter loan amount: "))
        loanQuery = "INSERT INTO loans (account_number, amount) VALUES (%s,%s)"
        myCursor.execute(loanQuery,(currentUser,loanAmount))
        myInfo.commit()
        print("pending")
        login()
def buy_recharge_card(currentUser):
        print('''
               press 1 for self recharge
               press 2 to recharge for others 
               press 3 to go back
               ''')
        choice = int(input("choose from the above: "))
        if choice == 1 : 
            selfCardQuery = f"SELECT * FROM recharge_cards WHERE PhoneNumber = {currentUser[5]}"
            myCursor.execute(selfCardQuery)
            selfInfo = myCursor.fetchone()
            rechargeCardAmount = Decimal(input("how much are willing to recharge: "))
                
            if selfInfo :
                remainingBalance = f"UPDATE accounts SET balance = balance - {rechargeCardAmount} WHERE account_number = {currentUser[0]}"
                myCursor.execute(remainingBalance)
                myInfo.commit()
                
                rechargeBalanceQuery = f"UPDATE recharge_cards SET amount = amount + {rechargeCardAmount} WHERE PhoneNumber = {currentUser[5]}"
                myCursor.execute(rechargeBalanceQuery)
                myInfo.commit()
                print("card recharged successfully")
                login()
            else :
                remainingBalance = f"UPDATE accounts SET balance = balance - {rechargeCardAmount} WHERE account_number = {currentUser[0]}"
                myCursor.execute(remainingBalance)
                myInfo.commit()
                query = "INSERT INTO recharge_cards (amount,PhoneNumber) VALUES (%s,%s)"
                myCursor.execute(query, (rechargeCardAmount,currentUser[5]))
                myInfo.commit()
                print("card recharged successfully")
                login()
        elif choice == 2:
            othersNumber = input("Enter the phone number you want to recharge")
            othersCardQuery = f"SELECT * FROM recharge_cards WHERE PhoneNumber = {othersNumber}"
            myCursor.execute(othersCardQuery)
            othersInfo = myCursor.fetchone()
            
            othersCardAmount = Decimal(input("how much are willing to recharge: "))
            if othersInfo:
                remainingBalance = f"UPDATE accounts SET balance = balance - {othersCardAmount} WHERE account_number = {currentUser[0]}"
                myCursor.execute(remainingBalance)
                myInfo.commit()
                rechargeBalanceQuery = f"UPDATE recharge_cards SET amount = amount + {othersCardAmount} WHERE PhoneNumber = {othersNumber}"
                myCursor.execute(rechargeBalanceQuery)
                myInfo.commit()
                print("card recharged successfully")
                login() 
                
            else:
                remainingBalance = f"UPDATE accounts SET balance = balance - {othersCardAmount} WHERE account_number = {currentUser[0]}"
                myCursor.execute(remainingBalance)
                myInfo.commit()
                rechargeOthersQuery = "INSERT INTO recharge_cards (amount,PhoneNumber) VALUES (%s,%s)"
                myCursor.execute(rechargeOthersQuery,(othersCardAmount,othersNumber))
                myInfo.commit()
                print("card recharged successfully")
                login()
                   
           
        elif choice == 3:
            login()
        else:
            print("Invalid input")
def transfer(payerAccNum):
        print('''
               press 1 to transfer
               press 2 to go back 
               ''')
        choice = int(input("choose from the above: "))
        if choice ==1:
            payerQuery  = f"SELECT *FROM accounts WHERE account_number = '{payerAccNum}'"
            myCursor.execute(payerQuery)
            payerInfo = myCursor.fetchone()
               
            transfer = input("input the account num ure transferring to: ")
            payeeQuery = f"SELECT * FROM accounts WHERE account_number = '{transfer}'"
            myCursor.execute(payeeQuery)
            payeeInfo = myCursor.fetchone()
                    
            transferAmount = Decimal(input("how much are you willing to transfer: "))
            if transferAmount <= payerInfo[2]:
                payerBalanceQuery = f"UPDATE accounts SET balance = balance - {transferAmount} WHERE account_number = {payerInfo[0]}"
                myCursor.execute(payerBalanceQuery)
                myInfo.commit()
                payerBalance = payerInfo[2] - transferAmount
                
                payeeBalanceQuery = f"UPDATE accounts SET balance = balance + {transferAmount} WHERE account_number = {transfer}"
                myCursor.execute(payeeBalanceQuery)
                myInfo.commit()
                print(f"Amount transfer successfully \nYour current balance is {payerBalance}")
                login()
            else: 
                    print("Insufficient balance")
        elif choice== 2:
            login()   
            
        else:
            print("Invalid input")     
           
def lock_money(currentUser):
        lockAmount = Decimal(input("Enter the amount you're willing to lock: "))
        if lockAmount <= currentUser[2]:
            lockQuery = f"UPDATE accounts SET locked_amount = locked_amount + {lockAmount},balance = balance - {lockAmount} WHERE account_number = {currentUser[0]}"
            myCursor.execute(lockQuery)
            myInfo.commit()
            print(f"N{lockAmount} lock successfully...")
            login()
        else:
            print('Insufficient balance')
def unlock_money(currentUser):
        unlockAmount = Decimal(input("Enter the amount you want to unlock: "))
        if unlockAmount <= currentUser[8]:
            unlockQuery = f"UPDATE accounts SET locked_amount = locked_amount - {unlockAmount},balance = balance + {unlockAmount} WHERE account_number = {currentUser[0]}"
            myCursor.execute(unlockQuery)
            myInfo.commit() 
            print(f"N{unlockAmount} unlock successfully")  
            login()        
        else:
            print("Insufficient balance ")    
def main():
    while True:
        print('''Welcome To Empress Bank
              
              Press '1' To create an account
              Press '2' To login
          ''')
        userInput = input("Kindly choose from the above: ")
        if userInput == '1':
            create_account()
        elif userInput == '2':
            login()
        else:
            print("invalid input")
            
main()


