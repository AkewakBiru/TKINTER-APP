import tkinter as tk
from PIL import ImageTk
import tkmacosx as mactk
from AdminManager import Admin
from tkinter import messagebox
from tkinter import ttk
import json
import datetime


class FitnessTrainer:
    """ Class to represent a Fitness Trainer's page (window) """

    # constructor
    def __init__(self, window):
        self.window = window
        self.style = ttk.Style()
        self.style.theme_use('aqua')
        self.tab = ttk.Notebook(self.window, width=600, height=550)
        self.tab.pack(expand=True, fill='both')

        self.frame1 = tk.Frame(self.tab, width=400, height=280, background="#E5E3E8")
        self.frame2 = tk.Frame(self.tab, width=400, height=280, background="#E5E3E8")

        self.frame1.pack(fill="both", expand=True)
        self.frame2.pack(fill="both", expand=True)

        self.tab.add(self.frame1, text="Schedule")
        self.tab.add(self.frame2, text="Profile")

        # tab 1 tkinter widgets
        self.add_scheduleBtn = ttk.Button(self.frame1, text="Add schedule", width=20, command=self.addSchedule)
        self.view_scheduleBtn = ttk.Button(self.frame1, text="View schedule", width=20, command=self.viewSchedule)

        self.scheduleWinCounter = 0
        self.viewScheWinCounter = 0

        self.add_scheduleBtn.pack(ipady=10, pady=20)
        self.view_scheduleBtn.pack(ipady=10, pady=20)

        # tab 2 tkinter widget
        self.btn = ttk.Button(self.frame2, text="view", width=30, command=self.display)
        self.btn.pack(ipady=10, pady=20)

        # Opens a window to add a schedule
    def addSchedule(self):
        if not self.scheduleWinCounter:
            self.schedulerWindow = tk.Toplevel(self.window)

            self.schedulerWindow.title("Membership")
            self.schedulerWindow.geometry('500x485+500+150')
            self.schedulerWindow.config(background="#E5E3E8")
            self.schedulerWindow.resizable(0, 0)

            self.schedulerWindow.protocol('WM_DELETE_WINDOW', self.on_schedule_exit)

            frame1 = tk.Frame(self.schedulerWindow, background="#E5E3E8")

            radiovar = tk.StringVar(frame1)
            checkvar1 = tk.StringVar(frame1)
            checkvar2 = tk.StringVar(frame1)
            checkvar3 = tk.StringVar(frame1)
            checkvar4 = tk.StringVar(frame1)
            checkvar5 = tk.StringVar(frame1)

            label = tk.Label(frame1, text=f"Choose suitable time to train", font="helvetica 20 bold",
                             background="#E5E3E8")
            label.pack(pady=20, padx=6)

            radio_frame = tk.Frame(frame1, background="#E5E3E8")
            radio_frame.pack()

            # radioButtons for choosing suitable time for training
            radio1 = tk.Radiobutton(radio_frame, text="6 AM - 8 AM", variable=radiovar, value=0)
            radio2 = tk.Radiobutton(radio_frame, text="8 AM - 10 AM", variable=radiovar, value=1)
            radio3 = tk.Radiobutton(radio_frame, text="10 AM - 12 PM", variable=radiovar, value=2)
            radio4 = tk.Radiobutton(radio_frame, text="12 PM - 4 PM", variable=radiovar, value=3)
            radio5 = tk.Radiobutton(radio_frame, text="4 PM - 6 PM", variable=radiovar, value=4)
            radio6 = tk.Radiobutton(radio_frame, text="6 PM - 8 PM", variable=radiovar, value=5)

            # radioButton placement
            radio1.grid(row=0, column=0, sticky="w", pady=10, padx=6)
            radio2.grid(row=0, column=1, sticky="w", pady=10, padx=6)
            radio3.grid(row=0, column=2, sticky="w", pady=10, padx=6)
            radio4.grid(row=1, column=0, sticky="w", pady=10, padx=6)
            radio5.grid(row=1, column=1, sticky="w", pady=10, padx=6)
            radio6.grid(row=1, column=2, sticky="w", pady=10, padx=6)

            dayLabel = tk.Label(frame1, text="Choose days to train", background="#E5E3E8", font="helvetica 20 bold")
            dayLabel.pack(pady=30, padx=6)

            check_frame = tk.Frame(frame1, background="#E5E3E8")
            check_frame.pack()

            # checkButtons for choosing suitable date for training
            checkbox1 = tk.Checkbutton(check_frame, text="Monday", variable=checkvar1, onvalue=1, offvalue=0)
            checkbox2 = tk.Checkbutton(check_frame, text="Tuesday", variable=checkvar2, onvalue=1, offvalue=0)
            checkbox3 = tk.Checkbutton(check_frame, text="Wednesday", variable=checkvar3, onvalue=1, offvalue=0)
            checkbox4 = tk.Checkbutton(check_frame, text="Thursday", variable=checkvar4, onvalue=1, offvalue=0)
            checkbox5 = tk.Checkbutton(check_frame, text="Friday", variable=checkvar5, onvalue=1, offvalue=0)

            # checkButton placement
            checkbox1.grid(row=0, column=0, sticky="w", pady=10, padx=6)
            checkbox2.grid(row=0, column=1, sticky="w", pady=10, padx=6)
            checkbox3.grid(row=0, column=2, sticky="w", pady=10, padx=6)
            checkbox4.grid(row=1, column=0, sticky="w", pady=10, padx=6)
            checkbox5.grid(row=1, column=1, sticky="w", pady=10, padx=6)

            frame1.pack()

            btn = ttk.Button(frame1, text="add",
                             command=lambda: self.getchoice([checkvar1.get(), checkvar2.get(), checkvar3.get(),
                                                             checkvar4.get(), checkvar5.get()], radiovar.get()), width=20)
            btn.pack(ipady=10, pady=20)

            self.scheduleWinCounter += 1

    # validates the choice a customer makes when adding a schedule and writes it to a file
    def getchoice(self, arg1, arg2):
        admin = Admin()
        if admin.readSchedule(uname) != "":
            messagebox.showinfo("showinfo", "You already have a schedule")
            return
        elif arg2 == "":
            messagebox.showerror("showerror", "You need to choose the time.")
            return
        elif "1" not in arg1:
            messagebox.showerror("showerror", "You need to choose at least one day")
            return
        elif admin.checkSchedule(uname):
            messagebox.showinfo("showinfo", "You already have a schedule")
            return
        else:
            schedule = f"{uname}, {arg2}, {arg1[0]}, {arg1[1]}, {arg1[2]}, {arg1[3]}, {arg1[4]}\n"
            admin.addSchedule(schedule)

    # destroys the schedulerWindow and resets the scheduleWinCounter attribute to 0 when the user clicks on 'X'
    def on_schedule_exit(self):
        self.schedulerWindow.destroy()
        self.scheduleWinCounter = 0

    # checks if a user has a schedule and if yes, then outputs it as a label on the screen.
    def viewSchedule(self):
        admin = Admin()
        if admin.checkSchedule(uname):
            frame = tk.Frame(self.frame1, background="#E5E3E8")
            frame.place(x=130, y=300)
            time, days = admin.readSchedule(uname)
            labelMsg = tk.Label(frame, text=f"Your Gym schedule is at \n{time} on {days}", background="#E5E3E8",
                                font="helvetica 16 bold")
            labelMsg.grid(row=0, column=0)
        else:
            messagebox.showerror("showerror", "You haven't added a schedule")

    # displays a user's profile
    def display(self):
        admin = Admin()
        line = admin.findLine(uname, 'AMUser.txt')

        Infn = admin.userRecords()[line - 1]
        addr = Infn[4].strip("\n")
        self.fname = tk.StringVar(self.frame2)

        self.profileFrame = tk.Frame(self.frame2, background="#E5E3E8")
        self.profileFrame.place(x=180, y=90)

        self.fnameLabel = tk.Label(self.profileFrame, text=f"Full name:", background="#E5E3E8")
        self.addr = tk.Label(self.profileFrame, text=f"Address:", background="#E5E3E8")
        self.phone = tk.Label(self.profileFrame, text=f"Phone Number:", background="#E5E3E8")
        self.email = tk.Label(self.profileFrame, text=f"Email Address:", background="#E5E3E8")

        # infn labels
        self.fnameVal = tk.Label(self.profileFrame, text=f"{Infn[0]}", background="#E5E3E8")
        self.addrVal = tk.Label(self.profileFrame, text=f"{Infn[2]}", background="#E5E3E8")
        self.phoneVal = tk.Label(self.profileFrame, text=f"{Infn[3]}", background="#E5E3E8")
        self.emailVal = tk.Label(self.profileFrame, text=f"{addr}", background="#E5E3E8")

        self.fnameLabel.grid(row=0, column=0, sticky="w", pady=5)
        self.addr.grid(row=1, column=0, sticky="w", pady=5)
        self.phone.grid(row=2, column=0, sticky="w", pady=5)
        self.email.grid(row=3, column=0, sticky="w", pady=5)

        self.fnameVal.grid(row=0, column=1, sticky="w", pady=5)
        self.addrVal.grid(row=1, column=1, sticky="w", pady=5)
        self.phoneVal.grid(row=2, column=1, sticky="w", pady=5)
        self.emailVal.grid(row=3, column=1, sticky="w", pady=5)
        return


class HeadTrainer:
    """ Class to represent the Head trainer page (window) """

    # constructor
    def __init__(self, window):
        self.window = window
        self.style = ttk.Style()
        self.style.theme_use('aqua')
        self.tab = ttk.Notebook(self.window, width=600, height=550)
        self.tab.pack(expand=True, fill='both')

        self.frame1 = tk.Frame(self.tab, width=400, height=280, background="#E5E3E8")
        self.frame2 = tk.Frame(self.tab, width=400, height=280, background="#E5E3E8")
        self.frame3 = tk.Frame(self.tab, width=400, height=280, background="#E5E3E8")
        self.frame4 = tk.Frame(self.tab, width=400, height=280, background="#E5E3E8")

        self.frame1.pack(fill="both", expand=True)
        self.frame2.pack(fill="both", expand=True)
        self.frame3.pack(fill="both", expand=True)
        self.frame4.pack(fill="both", expand=True)

        self.tab.add(self.frame1, text="Payment")
        self.tab.add(self.frame2, text="Schedule")
        self.tab.add(self.frame3, text="Records")
        self.tab.add(self.frame4, text="Profile")

        # tab 1 tkinter widgets
        self.unamePayment = tk.Label(self.frame1, text="Username", background="#E5E3E8")
        self.entryPayment = tk.Entry(self.frame1)
        self.viewPayBtn = ttk.Button(self.frame1, text="view payment", command=self.viewPayment)

        self.unamePayment.place(x=100, y=30)
        self.entryPayment.place(x=190, y=30)
        self.viewPayBtn.place(x=410, y=30)

        # tab 2 tkinter widgets
        self.uname = tk.Label(self.frame2, text="Username", background="#E5E3E8")
        self.entry = tk.Entry(self.frame2)
        self.btn = ttk.Button(self.frame2, text="view schedule", command=self.viewSchedule)

        self.uname.place(x=100, y=30)
        self.entry.place(x=190, y=30)
        self.btn.place(x=410, y=30)

        # tab 3 tkinter widgets
        self.view_users_win_counter = 0
        self.view_records_win_counter = 0
        self.delete_record_win_counter = 0
        self.view_trainers_win_counter = 0

        self.frameRecords = tk.Frame(self.frame3, background="#E5E3E8")
        self.frameRecords.pack()
        self.viewUsersBtn = ttk.Button(self.frameRecords, width=15, text="View usernames", command=self.viewUsers)
        self.viewRecordsBtn = ttk.Button(self.frameRecords, width=15, text="View records", command=self.viewRecords)
        self.printRecordsBtn = ttk.Button(self.frameRecords, width=15, text="Print records", command=self.printRecords)
        self.viewTrainersBtn = ttk.Button(self.frameRecords, width=15, text="View trainers", command=self.viewTrainers)

        self.viewUsersBtn.grid(row=0, column=0, ipady=10, pady=20, padx=10)
        self.viewRecordsBtn.grid(row=0, column=1, ipady=10, pady=20, padx=10)
        self.printRecordsBtn.grid(row=1, column=0, ipady=10, pady=20, padx=10)
        self.viewTrainersBtn.grid(row=1, column=1, ipady=10, pady=20, padx=10)

        # tab 5 tkinter widget
        self.btn = ttk.Button(self.frame4, text="view", width=30, command=self.display)
        self.btn.pack(ipady=10, pady=20)

    # views the latest payment a user has made
    def viewPayment(self):
        admin = Admin()
        line = admin.findLine(self.entryPayment.get(), "payment_logger.txt")

        if not line:
            # handle exception in case the profileFrame is not created
            try:
                self.profileFrame.destroy()
            except AttributeError:
                print("No profileFrame added")
            messagebox.showerror("showerror", "User doesn't have a payment record")
        else:
            record_line = admin.findLine(self.entryPayment.get(), 'AMUser.txt')
            Infn = admin.userRecords()[record_line - 1]
            memShip = admin.readMembership(self.entryPayment.get())[0]
            pay_record = admin.latestPayment(self.entryPayment.get())
            print(pay_record)
            fname = tk.StringVar(self.frame1)

            profileFrame = tk.Frame(self.frame1, background="#E5E3E8")
            profileFrame.place(x=180, y=90)

            fnameLabel = tk.Label(profileFrame, text=f"Full name:", background="#E5E3E8")
            memLabel = tk.Label(profileFrame, text=f"Membership:", background="#E5E3E8")
            dependant = tk.Label(profileFrame, text=f"Dependant:", background="#E5E3E8")
            amount = tk.Label(profileFrame, text=f"Amount:", background="#E5E3E8")
            date = tk.Label(profileFrame, text=f"Date:", background="#E5E3E8")

            # value labels
            fnameVal = tk.Label(profileFrame, text=f"{Infn[0]}", background="#E5E3E8")
            memVal = tk.Label(profileFrame, text=f"{memShip}", background="#E5E3E8")
            depVal = tk.Label(profileFrame, text=f"{pay_record[2]}", background="#E5E3E8")
            amtVal = tk.Label(profileFrame, text=f"{pay_record[1]} AED", background="#E5E3E8")
            dateVal = tk.Label(profileFrame, text=f"{pay_record[3]}", background="#E5E3E8")

            fnameLabel.grid(row=0, column=0, sticky="w", pady=5)
            memLabel.grid(row=1, column=0, sticky="w", pady=5)
            dependant.grid(row=2, column=0, sticky="w", pady=5)
            amount.grid(row=3, column=0, sticky="w", pady=5)
            date.grid(row=4, column=0, sticky="w", pady=5)

            fnameVal.grid(row=0, column=1, sticky="w", pady=5)
            memVal.grid(row=1, column=1, sticky="w", pady=5)
            depVal.grid(row=2, column=1, sticky="w", pady=5)
            amtVal.grid(row=3, column=1, sticky="w", pady=5)
            dateVal.grid(row=4, column=1, sticky="w", pady=5)
        return

    # views schedule of any person in the gym
    def viewSchedule(self):
        admin = Admin()
        line = admin.findLine(self.entry.get(), "AMSchedule.txt")

        if not line:
            # handle exception in case the profileFrame is not created
            try:
                self.profileFrame.destroy()
            except AttributeError:
                print("No profileFrame added")
            messagebox.showerror("showerror", "User doesn't have a schedule")
        else:
            time, days = admin.readSchedule(self.entry.get())
            record_line = admin.findLine(self.entry.get(), 'AMUser.txt')
            Infn = admin.userRecords()[record_line - 1]
            self.fname = tk.StringVar(self.frame2)

            self.profileFrame = tk.Frame(self.frame2, background="#E5E3E8")
            self.profileFrame.place(x=180, y=90)

            self.fnameLabel = tk.Label(self.profileFrame, text=f"Full name:", background="#E5E3E8")
            self.time = tk.Label(self.profileFrame, text=f"Time:", background="#E5E3E8")
            self.date = tk.Label(self.profileFrame, text=f"Date:", background="#E5E3E8")

            # infn labels
            self.fnameVal = tk.Label(self.profileFrame, text=f"{Infn[0]}", background="#E5E3E8")
            self.timeVal = tk.Label(self.profileFrame, text=f"{time}", background="#E5E3E8")
            self.dateVal = tk.Label(self.profileFrame, text=f"{days}", background="#E5E3E8")

            self.fnameLabel.grid(row=0, column=0, sticky="w", pady=5)
            self.time.grid(row=1, column=0, sticky="w", pady=5)
            self.date.grid(row=2, column=0, sticky="w", pady=5)

            self.fnameVal.grid(row=0, column=1, sticky="w", pady=5)
            self.timeVal.grid(row=1, column=1, sticky="w", pady=5)
            self.dateVal.grid(row=2, column=1, sticky="w", pady=5)
        return

    # displays all usernames on the window
    def viewUsers(self):
        admin = Admin()
        if not self.view_users_win_counter:
            self.viewUsersWin = tk.Toplevel(self.frame3, background="#E5E3E8")
            self.viewUsersWin.geometry("500x400+100+50")
            self.viewUsersWin.protocol('WM_DELETE_WINDOW', self.user_view_exit)
            self.viewUsersWin.title("Usernames")
            self.viewUsersWin.resizable(0, 0)

            containerFrame = tk.Frame(self.viewUsersWin, background="#E5E3E8")
            containerFrame.pack()
            label = tk.Label(containerFrame, text="Usernames", background="#E5E3E8", font="helvetica 16 bold")
            label.grid(row=0, columnspan=2, pady=10)
            users = admin.getuserInfo()[0]
            for i in range(len(users)):
                tk.Label(containerFrame, text=f"User {i+1}: ", background="#E5E3E8").grid(row=i+1, column=0, sticky="w")
                tk.Label(containerFrame, text=f"{users[i]}", background="#E5E3E8").grid(row=i+1, column=1, sticky="w")

            self.view_users_win_counter += 1
            self.viewUsersWin.mainloop()

    # destroys the viewUserWindow resets the window counter to 0
    def user_view_exit(self):
        self.view_users_win_counter = 0
        self.viewUsersWin.destroy()

    # displays all the user's record in a window
    def viewRecords(self):
        admin = Admin()
        if not self.view_records_win_counter:
            self.viewRecordsWin = tk.Toplevel(self.frame3, background="#E5E3E8")
            self.viewRecordsWin.geometry("650x500+100+50")
            self.viewRecordsWin.protocol('WM_DELETE_WINDOW', self.user_records_exit)
            self.viewRecordsWin.title("Records")
            self.viewRecordsWin.resizable(0, 0)

            containerFrame = tk.Frame(self.viewRecordsWin, background="#E5E3E8")
            containerFrame.pack()

            label = tk.Label(containerFrame, text="Records", background="#E5E3E8", font="helvetica 16 bold")
            label.grid(row=0, columnspan=5, pady=10)

            headers = ['Full Name', 'Position', 'Address', 'Phone Number', 'Email address']
            for i in range(len(headers)):
                tk.Label(containerFrame, text=f"{headers[i]}", background="#E5E3E8", font="helvetica 15 bold")\
                    .grid(row=1, column=i, padx=10, pady=10, sticky="w")

            records = admin.userRecords()
            for i in range(len(records)):
                record = records[i]
                email = record[-1].strip("\n")
                tk.Label(containerFrame, text=f"{record[0]}", background="#E5E3E8").\
                    grid(row=i+2, pady=10, padx=10, column=0, sticky="w")
                tk.Label(containerFrame, text=f"{record[1]}", background="#E5E3E8").\
                    grid(row=i+2, pady=10, padx=10, column=1, sticky="w")
                tk.Label(containerFrame, text=f"{record[2]}", background="#E5E3E8").\
                    grid(row=i+2, pady=10, padx=10, column=2, sticky="w")
                tk.Label(containerFrame, text=f"{record[3]}", background="#E5E3E8").\
                    grid(row=i+2, pady=10, padx=10, column=3, sticky="w")
                tk.Label(containerFrame, text=f"{email}", background="#E5E3E8").\
                    grid(row=i+2, pady=10, padx=10, column=4, sticky="w")

            self.view_records_win_counter += 1
            self.viewRecordsWin.mainloop()

    # destroys the viewRecordsWin window and resets the window counter 0
    def user_records_exit(self):
        self.view_records_win_counter = 0
        self.viewRecordsWin.destroy()

    # prints users record to the terminal console
    def printRecords(self):
        admin = Admin()
        records = admin.userRecords()
        for line in records:
            line[-1] = line[-1].strip("\n")
            print(line)
        messagebox.showinfo("showinfo", "Record is printed")

    def viewTrainers(self):
        admin = Admin()
        if not self.view_trainers_win_counter:
            self.viewTrainersWin = tk.Toplevel(self.frame3, background="#E5E3E8")
            self.viewTrainersWin.geometry("500x400+100+50")
            self.viewTrainersWin.protocol('WM_DELETE_WINDOW', self.trainer_view_exit)
            self.viewTrainersWin.title("Trainers")
            self.viewTrainersWin.resizable(0, 0)

            containerFrame = tk.Frame(self.viewTrainersWin, background="#E5E3E8")
            containerFrame.pack()
            label = tk.Label(containerFrame, text="Trainers", background="#E5E3E8", font="helvetica 16 bold")
            label.grid(row=0, columnspan=2, pady=10)
            trainers = admin.viewTrainers()
            for i in range(len(trainers)):
                tk.Label(containerFrame, text=f"Trainer {i + 1}: ", background="#E5E3E8").grid(row=i + 1, column=0,
                                                                                            sticky="w")
                tk.Label(containerFrame, text=f"{trainers[i]}", background="#E5E3E8").grid(row=i + 1, column=1, sticky="w")

            self.view_trainers_win_counter += 1
            self.viewTrainersWin.mainloop()

        # destroys the viewRecordsWin window and resets the window counter 0

    def trainer_view_exit(self):
        self.view_trainers_win_counter = 0
        self.viewTrainersWin.destroy()

# displays a user's profile
    def display(self):
        admin = Admin()
        line = admin.findLine(uname, 'AMUser.txt')

        Infn = admin.userRecords()[line - 1]
        addr = Infn[4].strip("\n")
        self.fname = tk.StringVar(self.frame4)

        self.profileFrame = tk.Frame(self.frame4, background="#E5E3E8")
        self.profileFrame.place(x=180, y=90)

        self.fnameLabel = tk.Label(self.profileFrame, text=f"Full name:", background="#E5E3E8")
        self.addr = tk.Label(self.profileFrame, text=f"Address:", background="#E5E3E8")
        self.phone = tk.Label(self.profileFrame, text=f"Phone Number:", background="#E5E3E8")
        self.email = tk.Label(self.profileFrame, text=f"Email Address:", background="#E5E3E8")

        # infn labels
        self.fnameVal = tk.Label(self.profileFrame, text=f"{Infn[0]}", background="#E5E3E8")
        self.addrVal = tk.Label(self.profileFrame, text=f"{Infn[2]}", background="#E5E3E8")
        self.phoneVal = tk.Label(self.profileFrame, text=f"{Infn[3]}", background="#E5E3E8")
        self.emailVal = tk.Label(self.profileFrame, text=f"{addr}", background="#E5E3E8")

        self.fnameLabel.grid(row=0, column=0, sticky="w", pady=5)
        self.addr.grid(row=1, column=0, sticky="w", pady=5)
        self.phone.grid(row=2, column=0, sticky="w", pady=5)
        self.email.grid(row=3, column=0, sticky="w", pady=5)

        self.fnameVal.grid(row=0, column=1, sticky="w", pady=5)
        self.addrVal.grid(row=1, column=1, sticky="w", pady=5)
        self.phoneVal.grid(row=2, column=1, sticky="w", pady=5)
        self.emailVal.grid(row=3, column=1, sticky="w", pady=5)
        return


class Dependant:
    """ Class to represent the Dependant's page (window) """

    # constructor
    def __init__(self, window):
        self.window = window
        self.style = ttk.Style()
        self.style.theme_use('aqua')
        self.tab = ttk.Notebook(self.window, width=600, height=550)
        self.tab.pack(expand=True, fill='both')

        self.frame1 = tk.Frame(self.tab, width=400, height=280, background="#E5E3E8")
        self.frame2 = tk.Frame(self.tab, width=400, height=280, background="#E5E3E8")

        self.frame1.pack(fill="both", expand=True)
        self.frame2.pack(fill="both", expand=True)

        self.tab.add(self.frame1, text="Account")
        self.tab.add(self.frame2, text="Profile")

        # tab 1 tkinter widgets
        self.topUpBtn = ttk.Button(self.frame1, text="Top up", width=20, command=self.TopUp)
        self.topUpBtn.pack(ipady=10, pady=20)

        # tab 2 tkinter widget
        self.btn = ttk.Button(self.frame2, text="view", width=30, command=self.display)
        self.btn.pack(ipady=10, pady=20)

        self.topLevels = 0

    # creates a window called top up to top up money to the account of the user
    def TopUp(self):
        if not self.topLevels:
            global topUpWindow
            topUpWindow = tk.Toplevel(self.frame1, background="#E5E3E8")
            topUpWindow.geometry("500x400+100+50")
            topUpWindow.protocol('WM_DELETE_WINDOW', self.top_up_exit)
            topUpWindow.title("Top Up")
            topUpWindow.resizable(0, 0)

            containerFrame = tk.Frame(topUpWindow, background="#E5E3E8")
            containerFrame.pack()

            amount = tk.Label(containerFrame, text="Amount", background="#E5E3E8")
            amount.grid(row=0, column=0, sticky="w", pady=50)

            amountEntry = tk.Entry(containerFrame)
            amountEntry.grid(row=0, column=1, pady=10)

            topBtn = ttk.Button(containerFrame, text="Top up", width=20,
                                command=lambda: self.depositMoney(amountEntry))
            topBtn.grid(row=2, column=1, ipady=10)

            self.topLevels += 1
            topUpWindow.mainloop()

    # deposits (tops up) money entered in the Entry box after validation
    def depositMoney(self, value):
        amount = value.get()
        admin = Admin()
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("showerror", "Enter a number")
            print("Enter a number")
        else:
            line = admin.findLine(uname, 'AMUser.txt')
            name = admin.readuserRecords()[line-1].split(", ")[0]

            cus_id = admin.getDepCreator(name)
            admin.modifyAmount(cus_id, amount)
            messagebox.showinfo("showinfo", f"You have topped up {amount} AED.\n"
                                            f"Your current balance is {admin.getCurrentBalance(cus_id)} AED")

    # destroys the depWindow and resets the topLevels attribute to 0 when the user clicks on 'X'
    def on_exit(self):
        depWindow.destroy()
        self.topLevels = 0

    # destroys the top up window created
    def top_up_exit(self):
        topUpWindow.destroy()
        self.topLevels = 0

    # displays a user's profile
    def display(self):
        admin = Admin()
        line = admin.findLine(uname, 'AMUser.txt')

        Infn = admin.userRecords()[line - 1]
        addr = Infn[4].strip("\n")
        self.fname = tk.StringVar(self.frame2)

        self.profileFrame = tk.Frame(self.frame2, background="#E5E3E8")
        self.profileFrame.place(x=180, y=90)

        self.fnameLabel = tk.Label(self.profileFrame, text=f"Full name:", background="#E5E3E8")
        self.addr = tk.Label(self.profileFrame, text=f"Address:", background="#E5E3E8")
        self.phone = tk.Label(self.profileFrame, text=f"Phone Number:", background="#E5E3E8")
        self.email = tk.Label(self.profileFrame, text=f"Email Address:", background="#E5E3E8")

        # infn labels
        self.fnameVal = tk.Label(self.profileFrame, text=f"{Infn[0]}", background="#E5E3E8")
        self.addrVal = tk.Label(self.profileFrame, text=f"{Infn[2]}", background="#E5E3E8")
        self.phoneVal = tk.Label(self.profileFrame, text=f"{Infn[3]}", background="#E5E3E8")
        self.emailVal = tk.Label(self.profileFrame, text=f"{addr}", background="#E5E3E8")

        self.fnameLabel.grid(row=0, column=0, sticky="w", pady=5)
        self.addr.grid(row=1, column=0, sticky="w", pady=5)
        self.phone.grid(row=2, column=0, sticky="w", pady=5)
        self.email.grid(row=3, column=0, sticky="w", pady=5)

        self.fnameVal.grid(row=0, column=1, sticky="w", pady=5)
        self.addrVal.grid(row=1, column=1, sticky="w", pady=5)
        self.phoneVal.grid(row=2, column=1, sticky="w", pady=5)
        self.emailVal.grid(row=3, column=1, sticky="w", pady=5)
        return


class CustomerPage:
    """ Class to represent a Customer's Window """
    # constructor
    def __init__(self, window):
        self.window = window
        self.style = ttk.Style()
        self.style.theme_use('aqua')
        self.tab = ttk.Notebook(self.window, width=600, height=550)
        self.tab.pack(expand=True, fill='both')

        self.frame1 = tk.Frame(self.tab, width=400, height=280, background="#E5E3E8")
        self.frame2 = tk.Frame(self.tab, width=400, height=280, background="#E5E3E8")
        self.frame3 = tk.Frame(self.tab, width=400, height=280, background="#E5E3E8")
        self.frame4 = tk.Frame(self.tab, width=400, height=280, background="#E5E3E8")

        self.frame1.pack(fill="both", expand=True)
        self.frame2.pack(fill="both", expand=True)
        self.frame3.pack(fill="both", expand=True)
        self.frame4.pack(fill="both", expand=True)

        self.tab.add(self.frame1, text="Choose Membership")
        self.tab.add(self.frame2, text="Schedule")
        self.tab.add(self.frame3, text="Account")
        self.tab.add(self.frame4, text="Profile")

        # tab 1 tkinter widgets
        self.memLabel = tk.Label(self.frame1, text="Choose membership", font="helvetica 20 bold", background="#E5E3E8")
        self.memLabel.pack(pady=30)

        self.Memframe = tk.Frame(self.frame1, background="#E5E3E8")
        self.Memframe.pack()

        self.goldBtn = ttk.Button(self.Memframe, text="Gold Membership", width=20,
                                  command=lambda: self.onButtonClick('b1'))
        self.silverBtn = ttk.Button(self.Memframe, text="Silver Membership", width=20,
                                    command=lambda: self.onButtonClick('b2'))
        self.bronzeBtn = ttk.Button(self.Memframe, text="Bronze Membership", width=20,
                                    command=lambda: self.onButtonClick('b3'))
        self.otherBtn = ttk.Button(self.Memframe, text="Others", width=20, command=lambda: self.onButtonClick('b4'))

        self.goldBtn.grid(row=0, column=0, pady=30, sticky="w", padx=30, ipady=10)
        self.silverBtn.grid(row=0, column=1, pady=30, sticky="w", padx=30, ipady=10)
        self.bronzeBtn.grid(row=1, column=0, pady=30, sticky="w", padx=30, ipady=10)
        self.otherBtn.grid(row=1, column=1, pady=30, sticky="w", padx=30, ipady=10)

        self.win_counter = 0

        # tab 2 tkinter widget
        self.add_scheduleBtn = ttk.Button(self.frame2, text="Add schedule", width=20, command=self.addSchedule)
        self.view_scheduleBtn = ttk.Button(self.frame2, text="View schedule", width=20, command=self.viewSchedule)

        self.scheduleWinCounter = 0
        self.viewScheWinCounter = 0

        self.add_scheduleBtn.pack(ipady=10, pady=20)
        self.view_scheduleBtn.pack(ipady=10, pady=20)

        # tab 3 tkinter widgets
        self.topLevels = 0  # attribute to keep track of window created
        self.dependantBtn = ttk.Button(self.frame3, text="Add dependant", width=20, command=self.Dependant)
        self.topUpBtn = ttk.Button(self.frame3, text="Top up", width=20, command=self.TopUp)
        self.payBtn = ttk.Button(self.frame3, text="Pay", width=20, command=self.paymentOption)

        self.dependantBtn.pack(ipady=10, pady=20)
        self.topUpBtn.pack(ipady=10, pady=20)
        self.payBtn.pack(ipady=10, pady=20)

        self.payWinCounter = 0

        # tab 4 tkinter widget
        self.btn = ttk.Button(self.frame4, text="view", width=30, command=self.display)
        self.btn.pack(ipady=10, pady=20)

        # reads the AMPackages_Prices.json file
    def json_loader(self, key):
        handler = open("AMPackages_Prices.json", "r")
        data = json.loads(handler.read())
        return data[key]

    # opens a window when a user chooses membership
    def onButtonClick(self, btn):
        admin = Admin()
        line = admin.findLine(uname, 'AMAccount.txt')
        if len(admin.readAccount()[line-1].split(", ")) == 3:
            if float(admin.readAccount()[line-1].strip("\n").split(", ")[2]) < 500:
                messagebox.showinfo("showinfo", "You need at least 500 AED to choose a Membership")
                return

        elif len(admin.readAccount()[line-1].split(", ")) < 3:
            messagebox.showinfo("showinfo", "You need to top up at least 500 AED to choose a Membership")
            return

        if not self.win_counter:
            self.MemdetailWindow = tk.Toplevel(self.window)
            self.MemdetailWindow.title("Membership")
            self.MemdetailWindow.geometry('400x200+500+250')
            self.MemdetailWindow.config(background="#E5E3E8")
            self.MemdetailWindow.resizable(0, 0)

            self.MemdetailWindow.protocol('WM_DELETE_WINDOW', self.on_mem_exit)

            self.package_frame = tk.Frame(self.MemdetailWindow, background="#E5E3E8")
            self.package_frame.pack()

            # if user clicks on the Gold Member button
            if btn == 'b1':
                data = self.json_loader('Gold Member')
                self.min_years = tk.Label(self.package_frame, text="Minimum years:", bg="#E5E3E8")
                self.min_yrs_val = tk.Label(self.package_frame, text=f"{data[0]['min_yrs']}", bg="#E5E3E8")

                self.max_yrs = tk.Label(self.package_frame, text="Maximum years:", bg="#E5E3E8")

                max_val = data[0]['max_yrs']
                if max_val == "":
                    max_val = "-"
                self.max_yrs_val = tk.Label(self.package_frame, text=f"{max_val}", bg="#E5E3E8")

                self.discountLabel = tk.Label(self.package_frame, text="Discount", bg="#E5E3E8")
                self.discount = tk.Label(self.package_frame, text=f"{data[0]['discount'] * 100}%", bg="#E5E3E8")

                self.min_years.grid(row=0, column=0, sticky="w", pady=5)
                self.min_yrs_val.grid(row=0, column=1, sticky="w", pady=5)

                self.max_yrs.grid(row=1, column=0, sticky="w", pady=5)
                self.max_yrs_val.grid(row=1, column=1, sticky="w", pady=5)

                self.discountLabel.grid(row=2, column=0, sticky="w", pady=5)
                self.discount.grid(row=2, column=1, sticky="w", pady=5)

                Mem_choose = tk.Button(self.MemdetailWindow, text="Confirm", width=15,
                                       command=lambda: self.writeMem('Gold Member'))
                Mem_choose.pack(ipady=10, pady=20)

            # if user clicks on the Silver member button
            if btn == 'b2':
                data = self.json_loader('Silver Member')
                self.min_years = tk.Label(self.package_frame, text="Minimum years", bg="#E5E3E8")
                self.min_yrs_val = tk.Label(self.package_frame, text=f"{data[0]['min_yrs']}", bg="#E5E3E8")

                self.max_yrs = tk.Label(self.package_frame, text="Maximum years", bg="#E5E3E8")

                max_val = data[0]['max_yrs']
                self.max_yrs_val = tk.Label(self.package_frame, text=f"{max_val}", bg="#E5E3E8")

                self.discountLabel = tk.Label(self.package_frame, text="Discount", bg="#E5E3E8")
                self.discount = tk.Label(self.package_frame, text=f"{data[0]['discount'] * 100}%", bg="#E5E3E8")

                self.min_years.grid(row=0, column=0, sticky="w", pady=5)
                self.min_yrs_val.grid(row=0, column=1, sticky="w", pady=5)

                self.max_yrs.grid(row=1, column=0, sticky="w", pady=5)
                self.max_yrs_val.grid(row=1, column=1, sticky="w", pady=5)

                self.discountLabel.grid(row=2, column=0, sticky="w", pady=5)
                self.discount.grid(row=2, column=1, sticky="w", pady=5)

                Mem_choose = tk.Button(self.MemdetailWindow, text="Confirm", width=15,
                                       command=lambda: self.writeMem('Silver Member'))
                Mem_choose.pack(ipady=10, pady=20)

            # if the user clicks on the Bronze Member button
            if btn == 'b3':
                data = self.json_loader('Bronze Member')
                self.min_years = tk.Label(self.package_frame, text="Minimum years", bg="#E5E3E8")
                self.min_yrs_val = tk.Label(self.package_frame, text=f"{data[0]['min_yrs']}", bg="#E5E3E8")

                self.max_yrs = tk.Label(self.package_frame, text="Maximum years", bg="#E5E3E8")

                max_val = data[0]['max_yrs']
                self.max_yrs_val = tk.Label(self.package_frame, text=f"{max_val}", bg="#E5E3E8")

                self.discountLabel = tk.Label(self.package_frame, text="Discount", bg="#E5E3E8")
                self.discount = tk.Label(self.package_frame, text=f"{data[0]['discount'] * 100}%", bg="#E5E3E8")

                self.min_years.grid(row=0, column=0, sticky="w", pady=5)
                self.min_yrs_val.grid(row=0, column=1, sticky="w", pady=5)

                self.max_yrs.grid(row=1, column=0, sticky="w", pady=5)
                self.max_yrs_val.grid(row=1, column=1, sticky="w", pady=5)

                self.discountLabel.grid(row=2, column=0, sticky="w", pady=5)
                self.discount.grid(row=2, column=1, sticky="w", pady=5)

                Mem_choose = tk.Button(self.MemdetailWindow, text="Confirm", width=15,
                                       command=lambda: self.writeMem('Bronze Member'))
                Mem_choose.pack(ipady=10, pady=20)

            # if the user clicks on the Others button
            if btn == 'b4':
                data = self.json_loader('Other')
                self.min_years = tk.Label(self.package_frame, text="Minimum years", bg="#E5E3E8")
                min_val = data[0]['min_yrs']
                if min_val == "":
                    min_val = "-"
                self.min_yrs_val = tk.Label(self.package_frame, text=f"{min_val}", bg="#E5E3E8")

                self.max_yrs = tk.Label(self.package_frame, text="Maximum years", bg="#E5E3E8")
                self.max_yrs_val = tk.Label(self.package_frame, text=f"{data[0]['max_yrs']}", bg="#E5E3E8")

                self.discountLabel = tk.Label(self.package_frame, text="Discount", bg="#E5E3E8")
                self.discount = tk.Label(self.package_frame, text=f"{data[0]['discount'] * 100}%", bg="#E5E3E8")

                self.min_years.grid(row=0, column=0, sticky="w", pady=5)
                self.min_yrs_val.grid(row=0, column=1, sticky="w", pady=5)

                self.max_yrs.grid(row=1, column=0, sticky="w", pady=5)
                self.max_yrs_val.grid(row=1, column=1, sticky="w", pady=5)

                self.discountLabel.grid(row=2, column=0, sticky="w", pady=5)
                self.discount.grid(row=2, column=1, sticky="w", pady=5)

                Mem_choose = tk.Button(self.MemdetailWindow, text="Confirm", width=15,
                                       command=lambda: self.writeMem('Other'))
                Mem_choose.pack(ipady=10, pady=20)

        self.win_counter += 1
        self.MemdetailWindow.mainloop()

    # appends the membership of a user to the AMUser.txt file
    def writeMem(self, membership):
        admin = Admin()
        # row (line) of a user to modify the membership
        line = admin.findLine(uname, 'AMUser.txt')
        AMusers = admin.readAMUser()
        memtype = membership
        checker = AMusers[line - 1].strip("\n").split(", ")

        # checks if a membership is already added
        try:
            assert len(checker) < 3
        except AssertionError:
            messagebox.showinfo("showinfo", "Membership already added")
        else:
            AMusers[line - 1] = AMusers[line - 1].strip("\n") + f", {memtype}\n"
            messagebox.showinfo("showinfo", f"Congrats, You are a {memtype}")

        admin.writeMembership(AMusers)

    # destroys the depWindow and resets the topLevels attribute to 0 when the user clicks on 'X'
    def on_mem_exit(self):
        self.MemdetailWindow.destroy()
        self.win_counter = 0

    # Opens a window to add a schedule
    def addSchedule(self):
        if not self.scheduleWinCounter:
            self.schedulerWindow = tk.Toplevel(self.window)

            self.schedulerWindow.title("Membership")
            self.schedulerWindow.geometry('500x485+500+150')
            self.schedulerWindow.config(background="#E5E3E8")
            self.schedulerWindow.resizable(0, 0)

            self.schedulerWindow.protocol('WM_DELETE_WINDOW', self.on_schedule_exit)

            frame1 = tk.Frame(self.schedulerWindow, background="#E5E3E8")

            radiovar = tk.StringVar(frame1)
            checkvar1 = tk.StringVar(frame1)
            checkvar2 = tk.StringVar(frame1)
            checkvar3 = tk.StringVar(frame1)
            checkvar4 = tk.StringVar(frame1)
            checkvar5 = tk.StringVar(frame1)

            label = tk.Label(frame1, text=f"Choose suitable time to train", font="helvetica 20 bold",
                             background="#E5E3E8")
            label.pack(pady=20, padx=6)

            radio_frame = tk.Frame(frame1, background="#E5E3E8")
            radio_frame.pack()

            # radioButtons for choosing suitable time for training
            radio1 = tk.Radiobutton(radio_frame, text="6 AM - 8 AM", variable=radiovar, value=0)
            radio2 = tk.Radiobutton(radio_frame, text="8 AM - 10 AM", variable=radiovar, value=1)
            radio3 = tk.Radiobutton(radio_frame, text="10 AM - 12 PM", variable=radiovar, value=2)
            radio4 = tk.Radiobutton(radio_frame, text="12 PM - 2 PM", variable=radiovar, value=3)
            radio5 = tk.Radiobutton(radio_frame, text="2 PM - 4 PM", variable=radiovar, value=4)
            radio6 = tk.Radiobutton(radio_frame, text="4 PM - 6 PM", variable=radiovar, value=5)

            # radioButton placement
            radio1.grid(row=0, column=0, sticky="w", pady=10, padx=6)
            radio2.grid(row=0, column=1, sticky="w", pady=10, padx=6)
            radio3.grid(row=0, column=2, sticky="w", pady=10, padx=6)
            radio4.grid(row=1, column=0, sticky="w", pady=10, padx=6)
            radio5.grid(row=1, column=1, sticky="w", pady=10, padx=6)
            radio6.grid(row=1, column=2, sticky="w", pady=10, padx=6)

            dayLabel = tk.Label(frame1, text="Choose days to train", background="#E5E3E8", font="helvetica 20 bold")
            dayLabel.pack(pady=30, padx=6)

            check_frame = tk.Frame(frame1, background="#E5E3E8")
            check_frame.pack()

            # checkButtons for choosing suitable date for training
            checkbox1 = tk.Checkbutton(check_frame, text="Monday", variable=checkvar1, onvalue=1, offvalue=0)
            checkbox2 = tk.Checkbutton(check_frame, text="Tuesday", variable=checkvar2, onvalue=1, offvalue=0)
            checkbox3 = tk.Checkbutton(check_frame, text="Wednesday", variable=checkvar3, onvalue=1, offvalue=0)
            checkbox4 = tk.Checkbutton(check_frame, text="Thursday", variable=checkvar4, onvalue=1, offvalue=0)
            checkbox5 = tk.Checkbutton(check_frame, text="Friday", variable=checkvar5, onvalue=1, offvalue=0)

            # checkButton placement
            checkbox1.grid(row=0, column=0, sticky="w", pady=10, padx=6)
            checkbox2.grid(row=0, column=1, sticky="w", pady=10, padx=6)
            checkbox3.grid(row=0, column=2, sticky="w", pady=10, padx=6)
            checkbox4.grid(row=1, column=0, sticky="w", pady=10, padx=6)
            checkbox5.grid(row=1, column=1, sticky="w", pady=10, padx=6)

            frame1.pack()

            btn = ttk.Button(frame1, text="add",
                             command=lambda: self.getchoice([checkvar1.get(), checkvar2.get(), checkvar3.get(),
                                                             checkvar4.get(), checkvar5.get()], radiovar.get()), width=20)
            btn.pack(ipady=10, pady=20)

            self.scheduleWinCounter += 1

    # validates the choice a customer makes when adding a schedule and writes it to a file
    def getchoice(self, arg1, arg2):
        admin = Admin()
        if admin.readSchedule(uname) != "":
            messagebox.showinfo("showinfo", "You already have a schedule")
            return
        if arg2 == "":
            messagebox.showerror("showerror", "You need to choose the time.")
            return
        elif "1" not in arg1:
            messagebox.showerror("showerror", "You need to choose at least one day")
            return
        elif admin.checkSchedule(uname):
            messagebox.showinfo("showinfo", "You already have a schedule")
            return
        else:
            schedule = f"{uname}, {arg2}, {arg1[0]}, {arg1[1]}, {arg1[2]}, {arg1[3]}, {arg1[4]}\n"
            admin.addSchedule(schedule)
            messagebox.showinfo("showinfo", "You have added a schedule")

    # destroys the schedulerWindow and resets the scheduleWinCounter attribute to 0 when the user clicks on 'X'
    def on_schedule_exit(self):
        self.schedulerWindow.destroy()
        self.scheduleWinCounter = 0

    # checks if a user has a schedule and if yes, then outputs it as a label on the screen.
    def viewSchedule(self):
        admin = Admin()
        if admin.checkSchedule(uname):
            frame = tk.Frame(self.frame2, background="#E5E3E8")
            frame.place(x=130, y=300)
            time, days = admin.readSchedule(uname)
            labelMsg = tk.Label(frame, text=f"Your Gym schedule is at \n{time} on {days}", background="#E5E3E8",
                                font="helvetica 16 bold")

            labelMsg.grid(row=0, column=0)
        else:
            messagebox.showerror("showerror", "You haven't added a schedule")

    # creates a window for dependant account management
    def Dependant(self):
        if not self.topLevels:
            global depWindow
            depWindow = tk.Toplevel(self.frame3, background="#E5E3E8")
            depWindow.geometry("500x400+100+50")
            depWindow.protocol('WM_DELETE_WINDOW', self.on_exit)
            depWindow.title("Dependant")
            depWindow.resizable(0, 0)

            depName = tk.Label(depWindow, text="Dependant Name", background="#E5E3E8")
            self.depEntry = tk.Entry(depWindow)
            depAddress = tk.Label(depWindow, text="Dependant Address", background="#E5E3E8")
            self.addrEntry = tk.Entry(depWindow)

            addBtn = mactk.Button(depWindow, text="Add", width=193, bg="#F1F1F1", activebackground="#BABABA", height=42,
                                  borderwidth=0, font=("helvetica", 14), command=self.addDependant)

            # place the widgets on the depWindow window
            depName.place(x=80, y=50)
            self.depEntry.place(x=220, y=50)

            depAddress.place(x=80, y=100)
            self.addrEntry.place(x=220, y=100)

            addBtn.place(x=220, y=150)

            self.topLevels += 1
            depWindow.mainloop()

    # validates entry inputs and adds user to the AMRecords.txt file
    def addDependant(self):
        admin = Admin()
        record = ""
        try:
            name = self.depEntry.get()
            assert len(name) > 1
        except AssertionError:
            messagebox.showerror("showerror", "Invalid name")
            return
        else:
            record += name + ", Dependant, "

        try:
            address = self.addrEntry.get()
            assert len(address) > 1
        except AssertionError:
            messagebox.showerror("showerror", "Invalid Address")
            return
        else:
            record += f"{address}, {uname}\n"

        # write to the AMDependant.txt file
        if admin.checkDependant(name):
            messagebox.showinfo("showinfo", "Dependant exists")
            return
        messagebox.showinfo("showinfo", "You have successfully added a dependant")
        admin.addDependant(record)

    # creates a window called top up to top up money to the account of the user
    def TopUp(self):
        if not self.topLevels:
            global topUpWindow
            topUpWindow = tk.Toplevel(self.frame3, background="#E5E3E8")
            topUpWindow.geometry("500x400+100+50")
            topUpWindow.protocol('WM_DELETE_WINDOW', self.top_up_exit)
            topUpWindow.title("Top Up")
            topUpWindow.resizable(0, 0)

            containerFrame = tk.Frame(topUpWindow, background="#E5E3E8")
            containerFrame.pack()

            amount = tk.Label(containerFrame, text="Amount", background="#E5E3E8")
            amount.grid(row=0, column=0, sticky="w", pady=50)

            amountEntry = tk.Entry(containerFrame)
            amountEntry.grid(row=0, column=1, pady=10)

            topBtn = ttk.Button(containerFrame, text="Top up", width=20, command=lambda: self.depositMoney(amountEntry))
            topBtn.grid(row=2, column=1, ipady=10)

            self.topLevels += 1
            topUpWindow.mainloop()

    # deposits (tops up) money entered in the Entry box after validation
    def depositMoney(self, value):
        amount = value.get()
        admin = Admin()
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("showerror", "Enter a number")
            print("Enter a number")
        else:
            admin.modifyAmount(uname, amount)
            messagebox.showinfo("showinfo", f"You have topped up {amount} AED.\n"
                                            f"Your current balance is {admin.getCurrentBalance(uname)} AED")

    # destroys the depWindow and resets the topLevels attribute to 0 when the user clicks on 'X'
    def on_exit(self):
        depWindow.destroy()
        self.topLevels = 0

    # destroys the top up window created
    def top_up_exit(self):
        topUpWindow.destroy()
        self.topLevels = 0

    # performs payment
    def paymentOption(self):

        # base payment price for customers
        PAYMENT = 100
        admin = Admin()
        print(admin.readMembership(uname)[1])
        if admin.readMembership(uname)[1] != 3:
            messagebox.showinfo("showinfo", "You haven't added a membership")
            return

        mem_type = admin.readMembership(uname)[0]
        if mem_type == "Gold Member":
            PAYMENT -= PAYMENT * 0.5
        elif mem_type == "Silver Member":
            PAYMENT -= PAYMENT * 0.25
        elif mem_type == "Bronze Member":
            PAYMENT -= PAYMENT * 0.1

        dep_num = admin.hasDependant(uname)
        if dep_num > 0:
            PAYMENT = PAYMENT * (dep_num+1)

        admin.payAmount(uname, PAYMENT)

        date = datetime.date.today()
        record = f"{uname}, {PAYMENT}, {dep_num}, {date}\n"
        admin.addPayment(record)

        messagebox.showinfo("showinfo", f"You have made a payment of {PAYMENT} AED\n"
                                        f"Your current balance is {admin.getCurrentBalance(uname)} AED")

    # displays a user's profile
    def display(self):
        admin = Admin()
        line = admin.findLine(uname, 'AMUser.txt')

        Infn = admin.userRecords()[line - 1]
        addr = Infn[4].strip("\n")
        self.fname = tk.StringVar(self.frame4)

        self.profileFrame = tk.Frame(self.frame4, background="#E5E3E8")
        self.profileFrame.place(x=180, y=90)

        self.fnameLabel = tk.Label(self.profileFrame, text=f"Full name:", background="#E5E3E8")
        self.addr = tk.Label(self.profileFrame, text=f"Address:", background="#E5E3E8")
        self.phone = tk.Label(self.profileFrame, text=f"Phone Number:", background="#E5E3E8")
        self.email = tk.Label(self.profileFrame, text=f"Email Address:", background="#E5E3E8")

        # infn labels
        self.fnameVal = tk.Label(self.profileFrame, text=f"{Infn[0]}", background="#E5E3E8")
        self.addrVal = tk.Label(self.profileFrame, text=f"{Infn[2]}", background="#E5E3E8")
        self.phoneVal = tk.Label(self.profileFrame, text=f"{Infn[3]}", background="#E5E3E8")
        self.emailVal = tk.Label(self.profileFrame, text=f"{addr}", background="#E5E3E8")

        self.fnameLabel.grid(row=0, column=0, sticky="w", pady=5)
        self.addr.grid(row=1, column=0, sticky="w", pady=5)
        self.phone.grid(row=2, column=0, sticky="w", pady=5)
        self.email.grid(row=3, column=0, sticky="w", pady=5)

        self.fnameVal.grid(row=0, column=1, sticky="w", pady=5)
        self.addrVal.grid(row=1, column=1, sticky="w", pady=5)
        self.phoneVal.grid(row=2, column=1, sticky="w", pady=5)
        self.emailVal.grid(row=3, column=1, sticky="w", pady=5)
        return


class Login:
    """ Class to represent the login page (window) """

    # constructor
    def __init__(self, window):
        self.window = window
        self.window.title("Log in")
        self.window.geometry("1350x700+0+0")
        self.window.config(bg="white")
        self.window.resizable(0, 0)

        # background image
        self.bg = ImageTk.PhotoImage(file="risen-wang-20jX9b35r_M-unsplash.jpg")

        self.Bigframe = tk.Frame(self.window).place(x=0, y=0)
        bg = tk.Label(self.Bigframe, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        # frames
        self.frame = tk.Frame(self.Bigframe, bg="#426980", width=550, height=400)
        self.frame.place(x=300, y=150)
        self.frame2 = tk.Frame(self.Bigframe, bg="white", width=250, height=400)
        self.frame2.place(x=850, y=150)

        # labels
        self.Label = tk.Label(self.frame, text="Login", fg="white", bg="#426980", font=("helvetica", 24, "bold")).place(x=250, y=50)

        # username label and entry box
        self.username = tk.Label(self.frame, text="Username", bg="#426980", fg="white")
        self.unameEntry = tk.Entry(self.frame, width=26)

        # password label and entry box
        self.password = tk.Label(self.frame, text="Password", bg="#426980", fg="white")
        self.pwdEntry = tk.Entry(self.frame, width=26)

        # submit button for submitting the form
        self.submitBtn = mactk.Button(self.frame, text="Log in", width=130, height=35, bg="#46AA64", fg="white",
                                      highlightcolor="#46AA64", highlightbackground="#46AA64",
                                      command=self.loginValidator)

        self.newUserlabel = tk.Label(self.frame2, text="New User?", fg="#46AA64", font=("helvetica", 24, "bold"))
        self.signUpBtn = mactk.Button(self.frame2, text="sign up", width=130, height=40, bg="#3A77BE", fg="white",
                                      font=("helvetica", 16, "bold"), command=self.signUp)

        self.newUserlabel.place(x=60, y=100)
        self.signUpBtn.place(x=60, y=170)

        self.username.place(x=140, y=120)
        self.unameEntry.place(x=240, y=115)

        self.password.place(x=140, y=170)
        self.pwdEntry.place(x=240, y=165)

        self.submitBtn.place(x=360, y=220)

    # validates the username and password entered by the user
    def loginValidator(self):
        global uname
        uname = self.unameEntry.get()
        pword = self.pwdEntry.get()

        admin = Admin()
        if admin.findUser(uname) is not False:
            password = admin.authenticate(admin.findUser(uname))
            hashedpwd = admin.hashpassword(pword)

            # compares the hash of the user who is attempting to login with the hash saved in the AMUser.txt file
            if hashedpwd == password:
                self.window.geometry("671x585+300+50")
                line = admin.findLine(uname, "AMUser.txt")

                print(admin.userRecords()[line - 1][1])
                if admin.userRecords()[line - 1][1] == "Customer":
                    self.window.title("Customer")
                    customer = CustomerPage(self.Bigframe)
                elif admin.userRecords()[line - 1][1] == "Dependant":
                    self.window.title("Dependant")
                    dependant = Dependant(self.Bigframe)
                elif admin.userRecords()[line - 1][1] == "Head Trainer":
                    self.window.title("Head Trainer")
                    head_trainer = HeadTrainer(self.Bigframe)
                elif admin.userRecords()[line - 1][1] == "Fitness Trainer":
                    self.window.title("Fitness Trainer")
                    fitness_trainer = FitnessTrainer(self.Bigframe)
                print(uname)
                return uname
            else:
                messagebox.askretrycancel("askretrycancel", "Incorrect password")
        elif len(uname) == 0:
            messagebox.showerror("showerror", "Username is required")
        else:
            messagebox.askretrycancel("askretrycancel", "Username doesn't exist")

    def signUp(self):
        self.window.destroy()
        import signup


# instance of the window class
window = tk.Tk()
# instance of the Login class
login = Login(window)
window.mainloop()

