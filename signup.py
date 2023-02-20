import random
import re
import string
import tkinter as tk
from tkinter import messagebox
import tkmacosx as mactk
from PIL import ImageTk
from AdminManager import Admin


class SignUp:
    """ Class to represent the SignUp window """
    # constructor
    def __init__(self, window):
        self.window = window
        self.window.title("Sign up page")
        self.window.geometry("1350x750+0+0")
        self.window.config(bg="white")
        self.window.resizable(0, 0)

        # background image
        self.bg = ImageTk.PhotoImage(file="../project/risen-wang-20jX9b35r_M-unsplash.jpg")
        bg = tk.Label(self.window, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        # frames
        self.frame = tk.Frame(self.window, bg="#426980", width=550, height=550)
        self.frame.place(x=300, y=100)
        self.frame2 = tk.Frame(self.window, bg="white", width=250, height=550)
        self.frame2.place(x=850, y=100)

        # labels
        self.Label = tk.Label(self.frame, text="Sign up", fg="white", bg="#426980", font=("helvetica", 24, "bold")). \
            place(x=250, y=30)

        self.fullname = tk.Label(self.frame, text="Full Name", fg="white", bg="#426980", font=("helvetica", 15))
        self.position = tk.Label(self.frame, text="Choose position", fg="white", bg="#426980", font=("helvetica", 15))
        self.address = tk.Label(self.frame, text="Address", fg="white", bg="#426980", font=("helvetica", 15))
        self.phoneNum = tk.Label(self.frame, text="Phone Number", fg="white", bg="#426980", font=("helvetica", 15))
        self.email = tk.Label(self.frame, text="Email address", fg="white", bg="#426980", font=("helvetica", 15))
        self.username = tk.Label(self.frame, text="Username", bg="#426980", fg="white", font=("helvetica", 15))
        self.password = tk.Label(self.frame, text="Password", bg="#426980", fg="white", font=("helvetica", 15))

        self.option = tk.StringVar(self.window)
        self.option.set("Customer")

        # entry boxes
        self.fnameEntry = tk.Entry(self.frame, width=26)
        self.options = tk.OptionMenu(self.frame, self.option, "Customer", "Fitness Trainer", "Head Trainer", "Dependant")
        self.options.config(width=24)
        self.addressEntry = tk.Entry(self.frame, width=26)
        self.phoneNumEntry = tk.Entry(self.frame, width=26)
        self.emailEntry = tk.Entry(self.frame, width=26)
        self.unameEntry = tk.Entry(self.frame, width=26)
        self.pwdEntry = tk.Entry(self.frame, width=26)

        # placement
        self.fullname.place(x=120, y=120)
        self.position.place(x=120, y=165)
        self.address.place(x=120, y=210)
        self.phoneNum.place(x=120, y=255)
        self.email.place(x=120, y=300)
        self.username.place(x=120, y=345)
        self.password.place(x=120, y=390)

        # Entry placement
        self.fnameEntry.place(x=240, y=120)
        self.options.place(x=240, y=165)

        self.addressEntry.place(x=240, y=210)
        self.phoneNumEntry.place(x=240, y=255)
        self.emailEntry.place(x=240, y=300)
        self.unameEntry.place(x=240, y=345)
        self.pwdEntry.place(x=240, y=390)

        # submit button for submitting the form
        self.submitBtn = mactk.Button(self.frame, text="Sign Up", width=160, height=40, bg="#46AA64", fg="white",
                                      highlightcolor="#46AA64", highlightbackground="#46AA64",
                                      font=("helvetica", 16, "bold"), command=self.saveUserInfo)

        self.msglabel = tk.Label(self.frame2, text="Have an account?", fg="#46AA64", font=("helvetica", 24, "bold"))
        self.loginBtn = mactk.Button(self.frame2, text="Log in", width=160, height=45, bg="#3A77BE", fg="white",
                                     font=("helvetica", 16, "bold"), command=self.logIn)

        self.resetBtn = mactk.Button(self.frame, text="Clear", width=120, height=30, bg="#46AA64", fg="white",
                                     highlightcolor="#46AA64", highlightbackground="#46AA64",
                                     font=("helvetica", 16, "bold"), command=self.reset)

        self.msglabel.place(x=23, y=150)
        self.loginBtn.place(x=45, y=220)

        self.submitBtn.place(x=325, y=450)
        self.resetBtn.place(x=120, y=458)

    # displays proper message for invalid user inputs
    def dispError(self, msg):
        messagebox.showerror("showerror", msg)

    # clears the entry boxes
    def reset(self):
        self.fnameEntry.delete(0, tk.END)
        self.addressEntry.delete(0, tk.END)
        self.phoneNumEntry.delete(0, tk.END)
        self.emailEntry.delete(0, tk.END)
        self.unameEntry.delete(0, tk.END)
        self.pwdEntry.delete(0, tk.END)

    # checks if a username exists and if not, calls another method in the Admin class to write a user's detail to a file
    def saveUserInfo(self):
        admin = Admin()
        userRecord = self.validateUserRecord()
        if userRecord != 0:
            loginRecord = self.validateLogin()
            if loginRecord != 0:
                account_id = self.createAccountID()
                admin.createUserRecord(loginRecord, userRecord, account_id)
                if userRecord.split(", ")[1] == "Dependant":
                    # modifies the AMDependant.txt file and adds the account id of the dependant
                    line = admin.findLine(userRecord.split(", ")[0], 'AMDependant.txt')
                    file = admin.readDependant()
                    fname = file[line-1].strip("\n").split(", ")[0]
                    pos = file[line-1].strip("\n").split(", ")[1]
                    acc_id = account_id
                    address = file[line-1].strip("\n").split(", ")[2]
                    cus_id = file[line-1].strip("\n").split(", ")[3]
                    modified = f"{fname}, {pos}, {acc_id}, {address}, {cus_id}\n"
                    file[line-1] = modified
                    admin.updateDependant(file)

            # updating the Membership of the dependant (inherits the same membership as the customer who added him/her
                    mem_type = admin.readMembership(cus_id)[0]
                    UserRecord = admin.readAMUser()
                    record_line = admin.findLine(loginRecord[0], 'AMUser.txt')
                    uname = UserRecord[record_line-1].split(", ")[0]
                    passwd = UserRecord[record_line-1].strip("\n").split(", ")[1]
                    mod_line = f"{uname}, {passwd}, {mem_type}\n"
                    UserRecord[record_line-1] = mod_line
                    admin.writeAMUser(UserRecord)

                    print(f"{mem_type}\n{passwd}\n{mod_line}")

    # validates user record detail information
    def validateUserRecord(self):
        admin = Admin()
        fname = self.fnameEntry.get()
        position = self.option.get()
        address = self.addressEntry.get()
        phoneNum = self.phoneNumEntry.get()
        email = self.emailEntry.get()

        if position == "Dependant":
            if not admin.findDependant(fname):
                self.dispError("There is no Dependant with that name")
                return 0

        # regex pattern to check the validity of an email address and a phone number
        emailPattern = r"\b[A-Za-z0-9]+@[A-Za-z0-9]+\.(com|net|org)\b"
        phonePattern = r"(\+971|0)\d{9}"

        if len(fname) < 2:
            self.dispError("First name should at least be 2 characters long.")
            return 0

        elif len(address) < 2:
            self.dispError("Invalid address")
            return 0

        elif re.fullmatch(phonePattern, phoneNum) is None:
            self.dispError("Invalid phone number")
            return 0

        elif re.fullmatch(emailPattern, email) is None:
            self.dispError("Invalid email address")
            return 0

        record = f"{fname}, {position}, {address}, {phoneNum}, {email}\n"
        return record

    # validates user login details
    def validateLogin(self):
        uname = self.unameEntry.get()
        password = self.pwdEntry.get()

        # an instance of the Admin class is needed for validating a username (if the username already exists)
        admin = Admin()
        if admin.findUser(uname) is not False:
            self.dispError("username already exists")
            return 0

        if len(uname) <= 1:
            self.dispError("username should at least be 2 characters long.")
            return 0
        if len(password) < 8:
            self.dispError("Minimum length of a password is 8 characters")
            return 0
        elif len(password) > 20:
            self.dispError("Password shouldn't exceed 20 characters")
            return 0
        elif re.search('[A-Z]', password) is None:
            self.dispError("Password should contain at least 1 uppercase letter")
            return 0
        elif re.search('[a-z]', password) is None:
            self.dispError("Password should contain at least 1 lowercase letter")
            return 0
        elif re.search('[0-9]', password) is None:
            self.dispError("Password should contain at least 1 number")
            return 0
        elif re.search('[!@#$%^&*()~`]', password) is None:
            self.dispError("Password should contain at least 1 special character")
            return 0

        hashedpwd = admin.hashpassword(password)
        record = f"{self.unameEntry.get()}"
        messagebox.showinfo("showinfo", "You have successfully created an account.")
        return record, hashedpwd

    # generate a random 5 digit character
    def createAccountID(self):

        # an instance of the Admin class is needed to check if the account ID generated is being used by another user.
        admin = Admin()
        acc_ids = admin.getuserInfo()[1]
        charset = string.ascii_uppercase + string.digits

        # if the generated random digit is in the AMUser.txt file generate another random digit
        while True:
            accound_id = ''.join(random.sample(charset, 5))
            if accound_id not in acc_ids:
                break
            continue
        return accound_id

    # destroys the current window and opens a new window.
    def logIn(self):
        self.window.destroy()
        import log_in


# instance of the Tk class
window = tk.Tk()

# instance of the Signup class
signup = SignUp(window)
window.mainloop()
