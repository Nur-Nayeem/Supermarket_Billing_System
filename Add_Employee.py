import os
import tkinter as tk
from tkinter import ttk
import customtkinter
from customtkinter import *
import sqlite3
from tkinter import messagebox
import re


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# MySQL Connection
db=sqlite3.connect('supermarket.db')
db.execute("CREATE TABLE IF NOT EXISTS employees(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, email TEXT, phone INT(11), address TEXT)")
cursor=db.cursor()
# insert
def insert():
    if (name_entry.get()=="" or email_entry.get()=="" or phone_entry.get()=="" or address_entry.get()==""):
        messagebox.showerror("Error","Please fill all the fields")
    else:
        reg_exp = r"^01\d{9}$"
        email_regex = r"^[^@]+@[^@]+\.[^@]+$"
        if not re.match(reg_exp, phone_entry.get()):
           messagebox.showerror("Error","Phone Number is not valid")
           return
        if not re.match(email_regex, email_entry.get()):
           messagebox.showerror("Error","Email is not valid")
           return
        details=[name_entry.get(),email_entry.get(),phone_entry.get(),address_entry.get()]
        cursor.execute("INSERT INTO employees (name, email, phone, address) VALUES(?,?,?,?)",details)
        db.commit()
        messagebox.showinfo("Success","Employee Added Successfully")
        display_data()

def clear():
    name_entry.delete(0,END)
    email_entry.delete(0,END)
    phone_entry.delete(0,END)
    address_entry.delete(0,END)

def fetch():
    cursor.execute("SELECT * FROM employees")
    rows=cursor.fetchall()
    return rows

def display_data():
    tv.delete(*tv.get_children())
    for row in fetch():
        tv.insert("",END,values=row)
        
def delete():
    selected_row=tv.focus()
    if selected_row:
        data=tv.item(selected_row)
        row=data["values"]
        id_entry=row[0]
        cursor.execute("DELETE FROM employees WHERE id=?",[id_entry])
        db.commit()
        messagebox.showinfo("Success","Employee Deleted Successfully")
        display_data()
    else:
        messagebox.showerror("Error","No Row Selected")

def get_data(event):
    clear()
    selected_row=tv.focus()
    data=tv.item(selected_row)
    row=data["values"]
    id_entry=row[0]
    name_entry.insert(0,row[1])
    email_entry.insert(0,row[2])
    phone_entry.insert(0,row[3])
    address_entry.insert(0,row[4])
    
def update():
    selected_row=tv.focus()
    if selected_row:
        data=tv.item(selected_row)
        row=data["values"]
        id_entry=row[0]
        reg_exp = r"^01\d{9}$"
        email_regex = r"^[^@]+@[^@]+\.[^@]+$"
        if not re.match(reg_exp, phone_entry.get()):
           messagebox.showerror("Error","Phone Number is not valid")
           return
        if not re.match(email_regex, email_entry.get()):
           messagebox.showerror("Error","Email is not valid")
           return
        new_details=[name_entry.get(),email_entry.get(),phone_entry.get(),address_entry.get(),id_entry]
        cursor.execute("UPDATE employees SET name=?,email=?,phone=?,address=? WHERE id=?",new_details)
        db.commit()
        messagebox.showinfo("Success","Employee Updated Successfully")
        display_data()
    else:
        messagebox.showerror("Error","No Row Selected")

def back():
    root.withdraw()
    os.system("python admin_page.py")
    root.destroy()
    os._exit(0)

# Start the mainloop.
# Create the custom Tkinter GUI.

root = customtkinter.CTk()
root.geometry("1000x600+400+120")
root.title("Add Employee")
root.config(bg="#17043d")
root.resizable(False, False)

font1=("Arial", 20, "bold")
font2=("Arial", 15, "bold")
font3=("Arial", 12, "bold")


# top fram
topMenueFram=CTkFrame(root,height=100)
topMenueFram.pack(side='top',fill='both')
bigFram=CTkFrame(root,width=980,height=390)
bigFram.pack(fill='both',expand=True)
frame1=customtkinter.CTkFrame(bigFram,fg_color='#FFFFFF',width=500,height=480)
frame1.place(x=350,y=0)
# top bar
backBtn=CTkButton(topMenueFram,text="BACK",cursor="hand2",command=back)
backBtn.place(x=10,y=10)

addemployeelbl=CTkLabel(topMenueFram,text="Add Employeed",font=font1)
addemployeelbl.place(x=400,y=10)




# Create a label for the name entry.
name_label = CTkLabel(bigFram, text="Name:")
name_label.place(x=20,y=20)

# Create an entry for the name.
name_entry = CTkEntry(bigFram)
name_entry.place(x=140,y=20)

# Create a label for the email entry.
email_label = CTkLabel(bigFram, text="Email:")
email_label.place(x=20,y=80)

# Create an entry for the email.
email_entry = CTkEntry(bigFram)
email_entry.place(x=140,y=80)

# Create a label for the phone entry.
phone_label = CTkLabel(bigFram, text="Phone:")
phone_label.place(x=20,y=140)

# Create an entry for the phone.
phone_entry = CTkEntry(bigFram)
phone_entry.place(x=140,y=140)

# Create a label for the address entry.
address_label = CTkLabel(bigFram, text="Address:")
address_label.place(x=20,y=200)

# Create an entry for the address.
address_entry = CTkEntry(bigFram)
address_entry.place(x=140,y=200)

# Create a button to register the employee.
save = CTkButton(bigFram, text="Add employee", font=font1,fg_color='#03a819',hover_color='#03a819',corner_radius=20,width=120,cursor='hand2',command=insert)
save.place(x=20,y=250)
update_btn=customtkinter.CTkButton(bigFram,text='Update',font=font1,fg_color='#b86512',hover_color='#b86512',corner_radius=20,width=120,cursor='hand2',command=update)
update_btn.place(x=200,y=250)
clear_btn=customtkinter.CTkButton(bigFram,text='Clear',font=font1,fg_color='#6e0e53',hover_color='#6e0e53',corner_radius=20,width=120,cursor='hand2',command=clear)
clear_btn.place(x=20,y=300)
delete_btn=customtkinter.CTkButton(bigFram,text='Delete',font=font1,fg_color='#cf061a',hover_color='#cf061a',corner_radius=20,width=120,cursor='hand2',command=delete)
delete_btn.place(x=200,y=300)


# treeview

style=ttk.Style()
style.configure('mystyle.Treeview',font=font3,rowheight=50)# modify the font of the body
style.configure('mystyle.Treeview.Heading',font=font3) #modify the font and heading
style.layout("mystyle.Treeview",[('mystyle.Treeview.treearea',{'sticky':'nswe'})]) #remove the border

tv=ttk.Treeview(frame1,columns=(1,2,3,4,5),show='headings',style='mystyle.Treeview')
tv.heading('1',text='ID')
tv.column('1',width=105)
tv.heading('2',text='Name')
tv.column('2',width=120)
tv.heading('3',text='Email')
tv.column('3',width=220)
tv.heading('4',text='Phone')
tv.column('4',width=150)
tv.heading('5',text='Address')
tv.column('5',width=150)
tv.bind('<ButtonRelease-1>',get_data)

tv.pack()
display_data()

root.mainloop()
