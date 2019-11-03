import sys
import os
# Create user class
class user(object):
    # Init all the attributes
    def __init__(self):

        self.transaction_summary_file = sys.argv[2]
        self.valid_account_list_file = sys.argv[1]
        self.function = ""
        self.mode = None
        self.login = False
        self.acctNum = ""
        self.acctName = None
        self.deposited = 0.00
        self.withdrawn = 0.00
        self.transferred = 0.00
        self.balance = 0.00

    # Ask user to login
    def userLogin(self):
        print("Welcome to use our bank system please select the following option")
        print("1. Login to an account(login):")
        print("2. Create an account (createacct)")
        print("3. Delete an account (deleteacct)")
        print("4. Deposit money into an account(deposit)")
        print("5. With draw money from an account(withdraw)")
        print("6. Transfer money from one account to the other (transfer)")
        print("7. Logging out(logout)")
        self.function = input("please enter your choice: \n")
        if self.function == "login":
            self.login = True
            self.userMode()
        else:
            print("Can not operate before login")
            return self.userLogin()

    # Ask user to choose mode
    def userMode(self):
        self.mode = input("Select mode: \n")
        if self.mode != "machine" and self.mode != "agent":
            print("error")
            return self.userLogin()
        else:
            self.login = True
            self.chooseFunction()

    # Ask user to choose the desired operation
    def chooseFunction(self):

        print("1. Create an account (createacct)")
        print("2. Delete an account (deleteacct)")
        print("3. Deposit money into an account(deposit)")
        print("4. With draw money from an account(withdraw)")
        print("5. Transfer money from one account to the other (transfer)")
        print("6. Logging out(logout)")
        self.function = input("Select function: \n")

        if self.login == False and self.function == "login":
            #Logged in
            self.login = True
            self.userLogin()
        elif self.function == "deposit" and self.login == True:
            self.deposit()
        elif self.function == "withdraw" and self.login == True:
            self.withdraw()
        elif self.function == "deleteacct" and self.login == True:
            self.deleteacct()
        elif self.function == "createacct" and self.login == True:
            self.createacct()
        elif self.function == "transfer" and self.login == True:
            self.transfer()
        elif self.function == "logout" and self.login == True:
            self.logout()
        else:
            print("ERROR function name")
            return self.chooseFunction()

    def logout(self):
        print("Logging out")
        self.writeSummary(self.transaction_summary_file, "EOS\n")
        # write transaction summary file()
        exit(0)

    # Check valid acc num
    def checkAccNum(self, accNum):
        if (int(accNum) // 1000000 > 0) and (int(accNum) // 1000000 < 10) and accNum.isdigit():
            return True
        return False

    # Check valid acc nam
    def checkAccName(self, accName):
        if len(accName) < 3 or len(accName) > 30:
            return False
        elif accName[0] == ' ' or accName[-1] == ' ':
            return False
        else:
            return True

    # Check valid transaction
    def checkAmount(self, amount):  # '400000'
        digitsOK = True
        if (len(amount) < 3) or (len(amount) > 8):
            digitsOK = False

        if self.function == "deposit" and digitsOK:
            if (self.mode == "machine" and int(amount) > 200000) or (self.deposited >= 500000):
                return False
            return True

        elif self.function == "withdraw" and digitsOK:
            if (self.mode == "machine" and int(amount) > 100000) or (self.withdrawn >= 500000):
                return False
        elif self.function == 'transfer' and digitsOK:
            if (self.mode == "machine" and int(amount) > 1000000) or (self.transferred >= 500000):
                return False
            return True
        # elif...


    def checkAccnumE(self, accNum):
            if accNum in self.fileOpen(self.valid_account_list_file):
                return True
            else:
                return False


    # Create a user account
    def createacct(self):
        if self.mode != "agent":
            print("error1")
            return 0
        else:
            acctNum = input("Please enter the account number: ")

            if acctNum not in self.fileOpen(self.valid_account_list_file) and self.checkAccNum(acctNum):
                print("Valid number")
                self.acctNum = acctNum
                self.acctName = input("Please enter the account name: ")
                print("Successfully create the account")
                self.fileAppend(self.valid_account_list_file, self.acctNum)
                content = "NEW " + self.acctNum + ' ' + '$0.00' + ' 0000000 ' + self.acctName + '\n'
                self.writeSummary(self.transaction_summary_file, content)
                return self.chooseFunction()
            else:
                print("Invalid ACCOUNT NUMBER")
                return self.createacct()

    # Delete a user account
    def deleteacct(self):
        accNumber = input("Please enter the number that you want to delete: ")
        if self.checkAccNum(accNumber) == True:
            list = self.fileOpen(self.valid_account_list_file)
            print(list)
            if accNumber in self.fileOpen(self.valid_account_list_file):
                accountName = input("Please enter the name of that account: ")
                if self.checkAccName(accountName) == True:
                    for i in range(len(list) - 1):
                        if accNumber == list[i]:
                            list.remove(list[i])
                    tempFile = open(self.valid_account_list_file, "w")
                    for line in list:
                        tempFile.write(line + "\n")
                    tempFile.close()
                    print("Account successfully deleted")
                    content = "DEL " + str(accNumber) + ' $0.00 ' + ' 0000000 ' + accountName + '\n'
                    self.writeSummary(self.transaction_summary_file, content)

                else:
                    return self.deleteacct()
        else:
            return self.deleteacct()

    # Deposit money into an account
    def deposit(self):
        # Enter deposit transaction
        self.function = "deposit"
        accountNumber = input("Enter acc num: \n")
        if accountNumber not in self.fileOpen(self.valid_account_list_file):
            print("deposit acc num error")
            return self.deposit()

        amount = input("Enter amount to be deposited: \n")
        while self.checkAmount(amount) == False:
            print("deposit amount error")
            amount = input("Enter amount to be deposited: ")


        self.deposited += float("{:.2f}".format(int(amount) / 100))
        print(str(int(self.deposited * 100)))
        if self.deposited <= 5000.0:
            print(str(self.deposited) + "deposited")
            self.balance += float("{:.2f}".format(int(amount) / 100))
            content = "DEP " + str(accountNumber) + ' ' + '$' + str(
                float("{:.2f}".format(int(amount) / 100))) + ' 0000000 ' + '***' + '\n'
            self.writeSummary(self.transaction_summary_file, content)
        else:
            print("Exceeded daily limit!")
        return self.chooseFunction()

    # Withdraw money from an account
    def withdraw(self):

        self.function = "withdraw"
        accountNumber = input("Enter acc num: ")
        while self.checkAccNum(accountNumber) == False:
            print("withdraw acc num error")
            return self.withdraw()

        amount = input("Enter amount to be withdrawn: ")
        while self.checkAmount(amount) == False:
            print("withdraw amount error")
            amount = input("Enter amount to be withdrawn: ")

        self.withdrawn += float("{:.2f}".format(int(amount) / 100))
        if (self.balance - self.withdrawn) < 0:
            print("No sufficient fund in account!")
        else:
            print(str(self.balance) + " withdrawn from account")
            content = "WDR " + str(accountNumber) + ' ' + '$' + str(
                float("{:.2f}".format(int(amount) / 100))) + ' 0000000 ' + '***' + '\n'
            self.writeSummary(self.transaction_summary_file, content)
        return self.chooseFunction()

    # Enter transfer transaction
        # Enter transfer transaction
    def transfer(self):
        self.function = "trasnfer"

        fromAcc = input("Enter the from acc num: ")
        while self.checkAccNum(fromAcc) == False or self.checkAccnumE(fromAcc) == False:
            print("invalid account number")
            fromAcc = input("Enter valid from acc num:")

        toAcc = input("Enter the to acc num: ")
        while self.checkAccNum(toAcc) == False or self.checkAccnumE(toAcc) == False:
            print("invalid to account number")
            toAcc = input("Enter valid to acc num:")

        if toAcc == fromAcc:
            print("Invalid to account number")
            return self.transfer()

        amount = input("Enter amount to transfer:")
        while self.checkAmount(amount) == False:
            print("invalid transfer amount ")
            amount = input("Enter amount to be deposited:")

        self.transferred += float("{:.2f}".format(int(amount) / 100))
        if (self.balance - self.transferred) < 0:
            print("Not sufficient fund")
        else:
            self.balance -= self.transferred
        #write to file
            content = "XFR " + str(toAcc) + ' ' + '$' + str(
                float("{:.2f}".format(int(amount) / 100))) + ' ' + str(fromAcc) + ' ' + '***' + '\n'
            self.writeSummary(self.transaction_summary_file, content)
        return self.chooseFunction()

    def fileOpen(self, filename):
        with open(filename) as f:
            lineList = [line.rstrip('\n') for line in open(filename)]
        f.close()
        return lineList

    def writeSummary(self, filename, content):
        tempFile = open(filename, "a")
        tempFile.write(content)
        tempFile.close()

    def fileAppend(self, filename, content):
        tempFile = open(filename, "r")
        accList = tempFile.readlines()
        for line in accList:
            line = line.strip()
        accList = accList[0:-1]
        accList.append(content)
        accList.append("\n0000000")
        tempFile = open(filename, "w")
        for line in accList:
            tempFile.write(line)
        tempFile.close()

if __name__ == "__main__":
    myUser = user()
    myUser.userLogin()