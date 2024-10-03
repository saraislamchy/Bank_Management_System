import random
from datetime import date

class UserClass:
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address

class History_Checker:
    def __init__(self, type, amount):
        self.type = type
        self.amount = amount
        self.date = date.today()

class User(UserClass):
    def __init__(self, name, email, address, account_type, password):
        super().__init__(name, email, address)
        self.account_type = account_type
        self.password = password
        self.balance = 0
        randomno = random.randint(1, 10000) 
        self.account_num = f"{00}{randomno}"
        self.loan_limit = 2
        self.transition_history = []

    def check_balance(self):
        return f"\nYour Account Balance is: {self.balance}tk\n"  

    def deposit(self, amount):
        self.balance += amount
        save_History = History_Checker('Deposit', amount)
        self.transition_history.append(save_History)
        print(f"\n- {amount}tk is successfully deposited on your account!")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            save_History = History_Checker('Withdraw', amount)
            self.transition_history.append(save_History)
            print(f"\nAmount of {amount}tk withdrawal is successful.")
        else:
            print("Withdrawal amount exceeded!!!")

    def transfer_money(self, bank_name, amount, account_number):
        if self.balance >= amount:
            for user in bank_name.users:
                if user.account_num == account_number: 
                    user.balance += amount
                    self.balance -= amount
                    save_History = History_Checker('Transfer money', amount)
                    self.transition_history.append(save_History)
                    print(f"{amount}tk successfully transferred to the account of '{user.name}'")
                    return
            print("\nAccount does not exist!!!")
        else:
            print(f"\nYour Transfer amount exceeded")

    def take_loan(self, bank_name, amount):
        if bank_name.loan_activity:
            if self.loan_limit > 0:
                self.balance += amount
                bank_name.loan_amount += amount
                self.loan_limit -= 1
                save_History = History_Checker('Loan', amount)
                self.transition_history.append(save_History)
                print(f"Congratulations! You got a loan of {amount}tk")
            else:
                print(f"Your loan limit is exceeded")
        else:
            print("Loan activity currently unavailable")

    def check_transition_history(self):
        print("\nTransaction history: ")
        for data in self.transition_history:
            print(f'- {data.type} \t| {data.amount}tk on {data.date}')

class Admin(UserClass):
    def __init__(self, name, email, address):
        super().__init__(name, email, address)

class Bank:
    def __init__(self, name):
        self.name = name
        self.__bank_balance = 1000000
        self.users = []
        self.admins = []
        self.loan_amount = 0
        self.loan_activity = True

    def check_balance(self):
        print(f"\n Total balance : {self.__bank_balance}tk")

    def view_loan_amount(self):
        print(f"\n- Total loan amount is: {self.loan_amount}tk")
    
    def remove_user(self, account_number):
        for user in self.users:
            if user.account_num == account_number:
                self.users.remove(user)
                print(f"\n{user.name} is removed.")
                return 
        print("Invalid user account number!!")

    def add_user(self, user_obj):
        self.users.append(user_obj)

    def add_admin(self, admin_obj):
        self.admins.append(admin_obj)
        print(f"- {admin_obj.name} added in admins data.")

    def find_user(self, bank_name, account_number, password):
        for user in bank_name.users:
            if user.account_num == account_number and user.password == password:
                return user
        else:
            return None    

    def find_admin(self, bank_name, name):
        for admin in bank_name.admins:
            if admin.name == name:
                return True
        else:
            return False
        
    def activate_loan(self, option):
        if option == 1:
            self.loan_activity = True
        elif option == 2:
            self.loan_activity = False
        else:
            print("Wrong command!!")  

    def view_admins(self):
        for admin in self.admins:
            print(f"Admin: {admin.name}, email: {admin.email}, address: {admin.address}")       

    def view_users(self):
        for user in self.users:
            print(f"User: {user.name}, {user.balance}tk, {user.account_type}, {user.account_num}")


abcbank = Bank("ABC Bank")
admin = Admin('Sara', "sara@gmail.com", 'Sylhet')
abcbank.admins.append(admin)

def UserPanel():
    while True:
        user = None
        print(f"------WELCOME TO {abcbank.name}------") 
        print("1. Login\n2. Create account\n3. Exit\n")
        opt = int(input("Choose an Option: "))
        if opt == 1:
            account_number = input("Enter your account number: ")
            password = input("Enter your password: ")
            find_user = abcbank.find_user(abcbank, account_number, password)
            if find_user is not None:
                user = find_user
                print(f"Successfully logged into your account")
            else:
                print(f"Invalid User!!")
                break
        elif opt == 2:
            if user is None:
                username = input("Enter your name: ")
                password = input("Create a password: ")
                email = input("Enter your email: ")
                address = input("Enter your address: ")
                print("\nAccount type: ")
                print("1. Savings\n2. Current")
                type = int(input("CHOOSE: "))
                accountType = 'Savings' if type == 1 else 'Current'
                user = User(username, email, address, accountType, password)
                abcbank.add_user(user)

        elif opt == 3:
            break

        if user:
            print(f"\n\n- WELCOME {user.name} to the '{abcbank.name}'")
            while True:
                print(f"\nYour account number is [{user.account_num}]")
                print("\nOptions:\n")
                print(f"1. Deposit\n2. Withdraw\n3. Transfer money\n4. Take loan - limit({user.loan_limit})\n5. Check balance\n6. Transaction history\n7. Exit")

                option = int(input("Choose your option: "))
                if option == 1:
                    user.deposit(int(input("Enter amount: ")))
                elif option == 2:
                    user.withdraw(int(input("Enter amount: ")))
                elif option == 3:
                    user.transfer_money(abcbank, int(input("Enter amount: ")), input("Receiver account number: "))
                elif option == 4:
                    user.take_loan(abcbank, int(input("Loan amount: ")))
                elif option == 5:
                    print(user.check_balance())
                elif option == 6:
                    user.check_transition_history()
                elif option == 7:
                    break
                else:
                    print("Invalid option!!")

def AdminPanel():
    while True:
        print("Choose your option:\n")
        print("1. Login\n2. Exit\n")
        option = int(input("Choose your option: "))
        if option == 1:
            searchadmin = input("Enter admin name: ")
            if abcbank.find_admin(abcbank, searchadmin):
                while True:
                    print("\nOptions:\n-")
                    print("1. View all users\n2. View all admins\n3. Delete user\n4. Total bank balance\n5. Total loan amount\n6. Loan status\n7. Add admin\n8. Exit")
                    
                    option = int(input("Choose your option: "))
                    if option == 1:
                        abcbank.view_users()
                    elif option == 2:
                        abcbank.view_admins()
                    elif option == 3:
                        abcbank.remove_user(input("User account number: "))
                    elif option == 4:
                        abcbank.check_balance()
                    elif option == 5:
                        abcbank.view_loan_amount()
                    elif option == 6:
                        print(f"Loan status: {'ON' if abcbank.loan_activity else 'OFF'}\n")  # Fixed quotation marks
                        print("Options: \n1. Turn on \n2. Turn off\n")
                        choice = int(input("Choose your option: "))
                        abcbank.activate_loan(choice)
                    elif option == 7:
                        adminname = input("Enter name: ")
                        email = input("Enter email: ")
                        address = input("Enter address: ")
                        admin = Admin(adminname, email, address)
                        abcbank.add_admin(admin)
                    elif option == 8:
                        break
            else:
                print("Admin not found")
                break
        else:
            break

while True:
    print("\nOptions: \n")
    print("1. User\n2. Admin\n3. Exit\n")
    option = int(input("Choose your option: "))
    if option == 1:
        UserPanel()
    elif option == 2:
        AdminPanel()
    elif option == 3:
        break
    else:
        print("Wrong command!!")
