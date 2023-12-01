import os
import customtkinter
from tkinter import messagebox
import sqlite3

db=sqlite3.connect('supermarket.db')
cursor = db.cursor() # databse er data python theke acces korar jonn

def registration():
    root.withdraw()
    os.system("python empreg.py")
    root.destroy()
    os._exit(0)

def login():
    username = entr1.get()
    password=entr2.get()
    if (entr1.get()=="" or entr2.get()==""):
        messagebox.showerror("Error","Please fill all the fields")
    else:
        # Check if the username and email match
        cursor.execute("SELECT * FROM employeeLogin WHERE name = ? AND password = ?", (username, password))
        if cursor.fetchone():
            messagebox.showinfo("Login Success", "Login successful!")
            entr1.delete(0, 'end')
            entr2.delete(0, 'end')
            root.withdraw()
            os.system("python main.py")
            root.destroy()
            os._exit(0)
        else:
            messagebox.showerror("Login Error", "Invalid username or password!")
    


customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

root=customtkinter.CTk()
root.title("Login as Employee")
root.geometry("500x400+550+250")


fram=customtkinter.CTkFrame(root)
fram.pack(fill="both", expand=True,padx=60, pady=20)

labl=customtkinter.CTkLabel(fram, text="Login", font=("Arial", 12))
labl.pack(padx=10, pady=10)
entr1=customtkinter.CTkEntry(fram,placeholder_text='Username')
entr1.pack(padx=10, pady=10)

entr2=customtkinter.CTkEntry(fram,placeholder_text='Password', show="*")
entr2.pack(padx=10, pady=12)

checkbox=customtkinter.CTkCheckBox(fram, text="Remember me")
checkbox.pack(padx=10, pady=10)

butt1=customtkinter.CTkButton(fram, text="Login", command=login)
butt1.pack(padx=10, pady=12)
butt2=customtkinter.CTkButton(fram, text="Self Registration", command=registration)
butt2.pack(padx=10, pady=12)

root.mainloop()