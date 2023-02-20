from hashlib import sha256
import json


class Admin:
    """ Class to represent an AdminManager """
    # constructor
    def __init__(self):
        pass

    # returns the list of usernames and passwords
    def getuserInfo(self):
        USERS = []
        PASSWORDS = []
        with open("AMUser.txt", "r") as users:
            for line in users:
                USERS.append(line.split(", ")[0])
                PASSWORDS.append(line.split(", ")[1].strip("\n"))
        return USERS, PASSWORDS

    # finds a user from the AMUser.txt file and returns true or false accordingly
    def findUser(self, user):
        users = self.getuserInfo()[0]
        try:
            return users.index(user)
        except ValueError:
            print("username not found")
            return False

    # hashes the password and returns the hash
    def hashpassword(self, password):
        hash = sha256()
        hash.update(password.encode('utf-8'))
        hashedpwd = hash.hexdigest()
        return hashedpwd

    # returns a password corresponding to a username
    def authenticate(self, index):
        pwords = self.getuserInfo()[1]
        return pwords[index]

    # writes user details to a file (username, password, account id and etc)
    def createUserRecord(self, log, record, acc_id):
        with open("AMUser.txt", "a") as login:
            login.write(f"{log[0]}, {log[1]}\n")

        with open("AMAccount.txt", "a") as acc_writer:
            acc_writer.write(f"{log[0]}, {acc_id}\n")

        with open("AMRecords.txt", "a") as Record:
            Record.write(f"{record}")

    # returns a list containing the records of a user by reading the AMRecords.txt file
    def userRecords(self):
        RECORDS = []
        with open("AMRecords.txt", "r") as record:
            for line in record:
                RECORDS.append(line.split(", "))
        return RECORDS

    # Reads the AMRecords.txt file and returns a list
    def readuserRecords(self):
        with open("AMRecords.txt", "r") as file:
            records = file.readlines()
        return records

    # writes teh AMRecords.txt file
    def writeuserRecords(self, data):
        with open("AMRecords.txt", "w") as file:
            file.writelines(data)

    # finds a row where a username is specified as an argument
    def findLine(self, uname, file):
        counter = 0
        with open(file, 'r') as handle:
            for line in handle:
                counter += 1
                if uname == line.split(", ")[0]:
                    return counter
            return False

    # reads the AMUser.txt file and returns the lines in a list
    def readAMUser(self):
        with open("AMUser.txt", "r") as file:
            lines = file.readlines()
        return lines

    # modifies a certain line and rewrites the whole file (since strings are immutable)
    def writeAMUser(self, record):
        with open("AMUser.txt", "w") as file:
            file.writelines(record)

    # writes the type of membership a user chooses
    def writeMembership(self, file):
        with open("AMUser.txt", "w") as fileWriter:
            fileWriter.writelines(file)

    # reads the membership record line of a customer from the AMUser.txt file
    def readMembership(self, uname):
        line = self.findLine(uname, 'AMAccount.txt')
        record = self.readAMUser()
        mem_type = record[line-1].strip("\n").split(", ")[-1]
        return mem_type, len(record[line-1].split(", "))

    # adds a dependant to the AMDependant.txt file
    def addDependant(self, row):
        with open("AMDependant.txt", "a") as file:
            file.write(row)

    # looks for a Dependant in the AMDependant.txt file and returns True if it finds it
    def findDependant(self, name):
        with open("AMDependant.txt", "r") as file:
            for line in file:
                if line.strip("\n").split(", ")[0] == name:
                    return True
            return False

    # checks duplicate dependant's name in the AMDependant.txt file
    def checkDependant(self, name):
        with open("AMDependant.txt", "r") as file:
            for line in file:
                if line.strip("\n").split(", ")[0] == name:
                    return True
            return False

    # returns the username that created the dependant
    def getDepCreator(self, name):
        record = self.readDependant()
        for line in record:
            if line.split(", ")[0] == name:
                uname = line.strip("\n").split(", ")[-1]
                return uname

    # read the AMDependant.txt file and return a list containing all entries (records) (lines)
    def readDependant(self):
        with open("AMDependant.txt", "r") as file:
            record = file.readlines()
        return record

    # modifies and rewrites the AMDependant.txt file
    def updateDependant(self, record):
        with open("AMDependant.txt", "w") as file:
            file.writelines(record)

    # checks how many dependants a customer has and returns the number
    def hasDependant(self, uname):
        counter = 0
        with open("AMDependant.txt", "r") as file:
            for line in file:
                if line.strip("\n").split(", ")[-1] == uname:
                    counter += 1
        return counter

    # finds a dependant's username
    def getDepUname(self, name):
        record = self.readDependant()
        acc_id = ''
        for line in record:
            if line.split(", ")[0] == name:
                acc_id = line.split(", ")[2]

        acc_id += "\n"
        acc_rec = self.readAccount()
        for line in acc_rec:
            if line.split(", ")[1] == acc_id:
                return line.split(", ")[0]

    # reads the file AMAccount.txt file and returns it as a list
    def readAccount(self):
        with open("AMAccount.txt", "r") as handle:
            records = handle.readlines()
        return records

    # modifies the amount of money a user owns in their account and writes it to the AMAccount.txt file
    def modifyAmount(self, uname, amount):
        index = self.findLine(uname, 'AMAccount.txt')
        Record = self.readAccount()
        line = Record[index - 1]

        checker = line.strip("\n").split(", ")

        try:
            assert len(checker) == 2
        except AssertionError:
            amount += float(line.strip("\n").split(", ")[2])
        finally:
            uname = Record[index - 1].strip('\n').split(', ')[0]
            acc_id = Record[index - 1].strip('\n').split(', ')[1]

            newRecord = f"{uname}, {acc_id}, {amount}\n"
            Record[index - 1] = newRecord
            self.AccountWrite(Record)

    # pay amount specified and update the AMAccount.txt file
    def payAmount(self, uname, amount):
        index = self.findLine(uname, 'AMAccount.txt')
        Record = self.readAccount()

        uname = Record[index - 1].strip('\n').split(', ')[0]
        acc_id = Record[index - 1].strip('\n').split(', ')[1]
        current = Record[index - 1].strip('\n').split(', ')[2]
        new_balance = float(current) - amount
        newRecord = f"{uname}, {acc_id}, {new_balance}\n"
        Record[index - 1] = newRecord
        self.AccountWrite(Record)

    # writes to the AMAccount.txt file
    def AccountWrite(self, data):
        with open("AMAccount.txt", "w") as handle:
            handle.writelines(data)

    # finds and returns the current balance of a Customer
    def getCurrentBalance(self, uname):
        line = self.findLine(uname, 'AMAccount.txt')
        balance = float(self.readAccount()[line - 1].strip("\n").split(", ")[2])
        return balance

    # adds schedule to the AMSchedule.txt file
    def addSchedule(self, schedule):
        with open("AMSchedule.txt", "a") as file:
            file.write(schedule)

    # checks if a user has a schedule, if they have returns True, if not it returns false
    def checkSchedule(self, uname):
        with open("AMSchedule.txt", "r") as file:
            for line in file:
                if line.split(", ")[0] == uname:
                    return True
            return False

    # reads the schedule and returns a notification message about the time and date of the schedule
    def readSchedule(self, uname):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        flag = 0
        with open("AMSchedule.txt", "r") as file:
            for line in file:
                if line.split(", ")[0] == uname:
                    record = line.strip("\n").split(", ")
                    flag = 1
                    break
            if flag == 0:
                return ""
        time = self.readJson()[record[1]]

        day = record[2:]
        training_days = ""
        for index in range(len(day)):
            if day[index] == "1":
                training_days += f", {days[index]}"
        return time, training_days

    # reads the AMSchedule.txt file and returns a list
    def viewSchedule(self):
        with open("AMSchedule.txt", "r") as file:
            record = file.readlines()
        return record

    # writes to the AMSchedule.txt file
    def writeSchedule(self, record):
        with open("AMSchedule.txt", "w") as file:
            file.writelines(record)

    # reads a json file and returns the data
    def readJson(self):
        handler = open("schedule_key.json", "r")
        data = json.loads(handler.read())
        return data

    # adds a payment to the payment_logger.txt file
    def addPayment(self, record):
        with open("payment_logger.txt", "a") as file:
            file.write(record)

    # read payment record
    def readPayment(self, uname):
        with open("payment_logger.txt", "r") as file:
            for line in file:
                if line.split(", ")[0] == uname:
                    return line.strip("\n").split(", ")

    # finds the latest payment of a user
    def latestPayment(self, uname):
        with open("payment_logger.txt", "r") as file:
            records = file.readlines()
        counter = len(records)-1
        while counter >= 0:
            if records[counter].split(", ")[0] == uname:
                return records[counter].strip("\n").split(", ")
            counter -= 1

    # returns the trainers
    def viewTrainers(self):
        trainers = []
        record = self.readuserRecords()
        for line in record:
            if line.split(", ")[1] == "Fitness Trainer":
                trainers.append(line.split(", ")[0])
        return trainers
