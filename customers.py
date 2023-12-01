import os
import tkinter as tk
from tkinter import ttk
import customtkinter
from customtkinter import *
import sqlite3
from tkinter import messagebox

# database
db=sqlite3.connect('supermarket.db')
cursor=db.cursor()

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")
# functions:

def fetch():
    cursor.execute("SELECT Billid,Total_Sell,Name,Mobile,Time FROM customers")
    rows=cursor.fetchall()
    return rows

def get_data():
    selected_row=treeview.focus()
    if selected_row:
        data=treeview.item(selected_row)
        row=data["values"]
        bill=int(row[0])
        return bill
    else:
        messagebox.showinfo("Error","Please select a row")
  
def update_view():
    # Connect to the MySQL database.
    db=sqlite3.connect('supermarket.db')
    cursor = db.cursor()

    # Get the table data from the database.
    cursor.execute(f"SELECT Billid,Total_Sell,Name,Mobile,Time FROM customers")
    table_data = cursor.fetchall()
    # Clear the treeview widget.
    treeview.delete(*treeview.get_children())

    # Insert the table data into the treeview widget.
    for row in table_data:
        treeview.insert("", tk.END, values=row)
    
    # Close the database connection.
    db.close()
    
def delete():
    bilArea.configure(frame2,state='normal')
    selected_row=treeview.focus()
    if selected_row:
        data=treeview.item(selected_row)
        row=data["values"]
        bill=row[0]
        if row:
           cursor.execute("DELETE FROM customers WHERE Billid=?",[bill])
           db.commit()
           messagebox.showinfo("Success","customers Deleted Successfully")
           update_view()
    else:
        messagebox.showinfo("Error","Please select a row")

def clear_bill():
    bilArea.configure(frame2,state='normal')
    bilArea.delete('1.0',END)
    
  
def view_bill():
    bilArea.configure(frame2,state='normal')
    bill=get_data()
    for i in os.listdir('bills/'):
        if i.split('.')[0]== str(bill):
            f=open(f'bills/{i}','r')
            bilArea.delete(1.0,END)
            for data in f:
                bilArea.insert(END,data)
            f.close()
            break
    else:
        messagebox.showerror("Error","Bill not found")
    bilArea.configure(frame2,state='disabled')
    

def back():
    root.withdraw()
    os.system("python admin_page.py")
    root.destroy()
    os._exit(0)


# main 
root = customtkinter.CTk()
root.geometry("1400x680+100+100")
root.title("Customers")
root.config(bg="#17043d")
root.resizable(False, False)


# top fram
topMenueFram=CTkFrame(root,height=100)
topMenueFram.pack(side='top',fill='both')
bigFram=CTkFrame(root,width=980,height=390)
bigFram.pack(fill='both',expand=True)
frame1=customtkinter.CTkFrame(bigFram,fg_color='#FFFFFF',width=800,height=480)
frame1.place(x=10,y=0)
frame2=customtkinter.CTkFrame(bigFram,width=500,height=470)
frame2.place(x=850,y=0)
# top bar
backBtn=CTkButton(topMenueFram,text="BACK",cursor="hand2",command=back)
backBtn.place(x=10,y=10)

addemployeelbl=CTkLabel(topMenueFram,text="Customers Details")
addemployeelbl.place(x=600,y=10)

bilArea=customtkinter.CTkTextbox(frame2,font=('times new roman',10),fg_color='white',width=400,height=280)
bilArea.place(x=40,y=30)

view_bill=CTkButton(frame2,text="View Bill",hover_color='#03a819',cursor="hand2",width=400,height=30,command=view_bill)
view_bill.place(x=40,y=320)
delete_bill=CTkButton(frame2,text="Delete Bill",fg_color='#cf061a',hover_color='#b86512',cursor="hand2",width=400,height=30,command=delete)
delete_bill.place(x=40,y=360)
delete_bill=CTkButton(frame2,text="Clear Bill",fg_color='#6e0e53',cursor="hand2",width=400,height=30,command=clear_bill)
delete_bill.place(x=40,y=400)

##Treeview widget data
style = ttk.Style()

# Configure the style to use a font size of 12.
style.configure("mystyle.Treeview", font=('Arial', 14))
style.configure('mystyle.Treeview.Heading',font=('Arial', 18,'bold'))
style.layout("mystyle.Treeview",[('mystyle.Treeview.treearea',{'sticky':'nwes'})])


table_data=fetch()

treeview = ttk.Treeview(frame1,columns=(1,2,3,4,5),show='headings',style='mystyle.Treeview',height=28,selectmode='extended')

# Add the headers to the treeview widget.
treeview["columns"] = ("Bill_Id", "Total_Sell","C_Name","Mobile","Shopping_Time")
treeview.heading("Bill_Id", text="Bill_Id",)
treeview.heading("Total_Sell", text="Total_Sell")
treeview.heading("C_Name", text="C_Name")
treeview.heading("Mobile", text="Mobile")
treeview.heading("Shopping_Time", text="Shopping_Time")
# Insert the table data into the treeview widget.
for row in table_data:
    treeview.insert("", tk.END, values=row)


# Remove the `Product ID` column from the treeview widget.
treeview["displaycolumns"] = ("Bill_Id", "Total_Sell","C_Name","Mobile","Shopping_Time")
# Set the `columnconfigure` method for the treeview widget to remove the space.
treeview.columnconfigure(0, weight=1)
treeview.columnconfigure(1, weight=1)
treeview.columnconfigure(2, weight=1)
treeview.columnconfigure(3, weight=1)
treeview.columnconfigure(4, weight=1)
# treeview.bind('<ButtonRelease-1>',get_data)


# Pack the treeview widget.
scrollbar = ttk.Scrollbar(frame1, orient="vertical", command=treeview.yview)
treeview.config(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
treeview.pack(side='right',fill='both', expand=True)




root.mainloop()