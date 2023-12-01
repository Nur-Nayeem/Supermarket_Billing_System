import os
import customtkinter
from tkinter import messagebox
import sqlite3
import re

db=sqlite3.connect('supermarket.db')
cursor = db.cursor()

def back_to_login():
    root.withdraw()
    os.system("python emplogin.py")
    root.destroy()
    os._exit(0)

def register():
    username = entr1.get()
    email=entr2.get()
    password=entr3.get()
    if (entr1.get()=="" or entr2.get()=="" or entr3.get()==""):
        messagebox.showerror("Error","Please fill all the fields")
    else:
        email_regex = r"^[^@]+@[^@]+\.[^@]+$"
        if not re.match(email_regex, entr2.get()):
            messagebox.showerror("Error","Email is not valid")
            return
        # Check if the username and email match
        cursor.execute("SELECT * FROM employees WHERE name = ? AND email = ?", (username, email))
        if cursor.fetchone():
            db.execute("CREATE TABLE IF NOT EXISTS employeeLogin(name TEXT,password TEXT)")
            cursor.execute("INSERT INTO employeeLogin (name, password) VALUES(?,?)",(username,password))
            db.commit()
            messagebox.showinfo("Register Success", "Registration successful!")
            entr1.delete(0, 'end')
            entr2.delete(0, 'end')
            entr3.delete(0, 'end')
            root.withdraw()
            os.system("python emplogin.py")
            root.destroy()
            os._exit(0)
        else:
            messagebox.showerror("register Error", "You are not an employee!")

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

root=customtkinter.CTk()
root.title("Login as Employee")
root.geometry("500x400+550+250")


fram=customtkinter.CTkFrame(root)
fram.pack(fill="both", expand=True,padx=60, pady=20)

labl=customtkinter.CTkLabel(fram, text="Self Registration", font=("Arial", 12))
labl.pack(padx=10, pady=10)
entr1=customtkinter.CTkEntry(fram,placeholder_text='Username')
entr1.pack(padx=10, pady=10)

entr2=customtkinter.CTkEntry(fram,placeholder_text='Email')
entr2.pack(padx=10, pady=12)

entr3=customtkinter.CTkEntry(fram,placeholder_text='Password', show="*")
entr3.pack(padx=10, pady=12)

butt1=customtkinter.CTkButton(fram, text="Register", command=register)
butt1.pack(padx=10, pady=12)

butt2=customtkinter.CTkButton(fram, text="Back to login", command=back_to_login)
butt2.pack(padx=10, pady=12)

root.mainloop()