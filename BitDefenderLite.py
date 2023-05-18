import os.path
import pygame
from cryptography.fernet import Fernet
from tkinter import Tk, messagebox
from collections import Counter
import tkinter


# all 10 characters of username and password need to be unique
def is_Unique_Entry():
    if (len(Counter(usrname.get())) >= 10) and (len(password.get()) >= 10):
        if (usrname.get().find("|") == -1) and (password.get().find("|") == -1):
            return True
    if (usrname.get().find("|") != -1) or (password.get().find("|") != -1):
        messagebox.showinfo(
            title="Error", message="Cannot use the symbol '|'")
        return False
    if (len(Counter(usrname.get())) < 10) or (len(password.get()) < 10):
        messagebox.showinfo(
            title="Error", message="10 Unique Characters are required")
        return False


# load the key
def load_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key


# write the key
def write_key():
    # if key.key file doesnt exist in directory, write_key(): is called
    #  and compiled once, THEN THE CALL to "write_key():" IS REMOVED
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def add_btnn():
    if is_Unique_Entry() and does_File_Exist('./passwords.txt'):
        with open('passwords.txt', 'r') as file:
            # for loop for number of lines
            # if file is not empty the for loop runs
            for line in file.readlines():
                data = line.rstrip()
                user, passw = data.split("|")
                # leave for loop if u find duplicate
                if usrname.get() == user:
                    messagebox.showinfo(
                        title="Error", message="Username Taken.")
                    return
        with open('passwords.txt', 'a') as f:
            f.write(usrname.get() + "|" + fer.encrypt(password.get().encode()).decode()
                    + "\n")


def create_new_window():
    jFrame.destroy()
    jFrame2 = Tk(className="\Encryption Key")
    jFrame2.resizable(0, 0)
    jFrame2.configure(bg="#333334")
    # creating properties
    login_title2 = tkinter.Label(
        jFrame2, text="Here is your Two Factor Authentication Key:", fg="#FF3380", bg="#333334", font=("Arial", 28))
    # adding properties
    key_lbl = tkinter.Label(jFrame2, text=passw,
                            bg="#333334", fg="white", font=("Arial", 16), wraplength=700)
    login_title2.place(relx=0.5, rely=0.3, anchor="center")
    key_lbl.place(relx=0.5, rely=0.6, anchor="center")
    jFrame2.geometry(f"800x200+{(ws-800)//2}+{(hs-200)//2}")


def login_btnn():
    global passw
    if is_Unique_Entry() and does_File_Exist('./passwords.txt'):
        # if file is empty
        if os.path.getsize('passwords.txt') == 0:
            messagebox.showinfo(title="Error", message="No user found.")
            return
        with open('passwords.txt', 'r') as file:
            # if file is not empty the for loop runs
            for line in file.readlines():
                data = line.rstrip()
                user, passw = data.split("|")
                if (usrname.get() == user) and (password.get() == fer.decrypt(passw.encode()).decode()):
                    create_new_window()  # create new window
                    return
        messagebox.showinfo(title="Error", message="No user found.")


key = load_key()
fer = Fernet(key)


def does_File_Exist(filePathAndName):
    return os.path.exists(filePathAndName)


pygame.init()

jFrame = Tk(className="\Login")

# acts like Java jFrame
jFrame.resizable(0, 0)
jFrame.configure(bg="#333334")

# creating properties
login_title = tkinter.Label(
    jFrame, text=" Bit Defender Lite", fg="#FF3380", bg="#333334", font=("Arial", 30))
usrname_lbl = tkinter.Label(jFrame, text="Username:",
                            bg="#333334", fg="white", font=("Arial", 16))
usrname = tkinter.Entry(jFrame, bg="white", font=("Arial", 16))
password = tkinter.Entry(jFrame, show="●", bg="white", font=("Arial", 16))
password_lbl = tkinter.Label(
    jFrame, text="Password:", bg="#333334", fg="white", font=("Arial", 16))

# add view login btns
add_btn = tkinter.Button(jFrame, text="Add", bg="#FF3380", font=(
    "Arial", 16), fg="white", command=add_btnn, padx=10)
login_btn = tkinter.Button(jFrame, text="Login", bg="#FF3380", font=(
    "Arial", 16), fg="white", command=login_btnn)

# adding properties
login_title.grid(row=0, column=0, columnspan=2, pady=40)
usrname_lbl.grid(row=1, column=0, padx=10, sticky="w")
usrname.grid(row=1, column=1, pady=10)
password_lbl.grid(row=2, column=0, padx=10, sticky="w")
password.grid(row=2, column=1, pady=10)

# add view login btns
add_btn.place(relx=0.4, rely=0.8, anchor="center")
login_btn.place(relx=0.6, rely=0.8, anchor="center")

# get the size of window
# width of the screen
ws = jFrame.winfo_screenwidth()
# height of the screen
hs = jFrame.winfo_screenheight()

# w, h, x, y
jFrame.geometry(f"400x330+{(ws-400)//2}+{(hs-330)//2}")
jFrame.mainloop()
