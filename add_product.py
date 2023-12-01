import os
import mysql.connector
from tkinter import *
from tkinter import ttk
import tkinter as tk
import customtkinter
from tkinter import messagebox
from CTkListbox import *
from customtkinter import *
import sqlite3


# MySQL Connection
db=sqlite3.connect('supermarket.db')
cursor = db.cursor()

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

def update_adding():
    # Connect to the MySQL database.
    db=sqlite3.connect('supermarket.db')
    cursor = db.cursor()

    # Get the table data from the database.
    cursor.execute(f"SELECT * FROM products1")
    table_data1 = cursor.fetchall()
    cursor.execute(f"SELECT * FROM products2")
    table_data2 = cursor.fetchall()
    cursor.execute(f"SELECT * FROM products3")
    table_data3 = cursor.fetchall()
    # Clear the treeview widget.
    treeview.delete(*treeview.get_children())

    # Insert the table data into the treeview widget.
    for row in table_data1:
        treeview.insert("", tk.END, values=row)
    
    for row in table_data2:
        treeview.insert("", tk.END, values=row)
    
    for row in table_data3:
        treeview.insert("", tk.END, values=row)

    # Close the database connection.
    db.close()

def add_prod1():
    name = combobox1.get()
    if(addstasionaryqnty.get()!=""):
        quantity = int(addstasionaryqnty.get())
         # Insert the new product into the database.
        try:
          cursor.execute("UPDATE products1 SET quantity = quantity + ? WHERE name = ?", [quantity, name])
          db.commit()
        except Exception as e:
          messagebox.showerror("Error", "Failed to add product: {}".format(e))
          return

        # Show a success message.
        messagebox.showinfo("Success", "Product added successfully!")

        # Clear the user input fields.
        addstasionaryqnty.delete(0, END)
    elif(addstasionaryDiscount.get()!=""):
        discount = float(int(addstasionaryDiscount.get())/100)
        try:
          cursor.execute("UPDATE products1 SET discount = ? WHERE name = ?", [discount, name])
          cursor.execute("UPDATE products1 SET discount_price = price - (price * ? ) WHERE name = ?", [discount, name])
          db.commit()
        except Exception as e:
          messagebox.showerror("Error", "Failed to add discount: {}".format(e))
          return
        messagebox.showinfo("Success", "Discount added successfully!")
        addstasionaryDiscount.delete(0, END)
    else:
      messagebox.showerror("Error", "Please enter a valid quantity.")
      return
    update_adding()
    
    

def add_prod2():
    name = combobox2.get()
    if(addgroceryqnty.get()!=""):
        quantity = int(addgroceryqnty.get())
         # Insert the new product into the database.
        try:
          cursor.execute("UPDATE products2 SET quantity = quantity + ? WHERE name = ?", [quantity, name])
          db.commit()
        except Exception as e:
          messagebox.showerror("Error", "Failed to add product: {}".format(e))
          return

        # Show a success message.
        messagebox.showinfo("Success", "Product added successfully!")

        # Clear the user input fields.
        addgroceryqnty.delete(0, END)
    elif(addgroceryDiscount.get()!=""):
        discount = float(int(addgroceryDiscount.get())/100)
        try:
          cursor.execute("UPDATE products2 SET discount = ? WHERE name = ?", [discount, name])
          cursor.execute("UPDATE products2 SET discount_price = price - (price * ? ) WHERE name = ?", [discount, name])
          db.commit()
        except Exception as e:
          messagebox.showerror("Error", "Failed to add discount: {}".format(e))
          return
        messagebox.showinfo("Success", "Discount added successfully!")
        addgroceryDiscount.delete(0, END)
    else:
      messagebox.showerror("Error", "Please enter a valid quantity.")
      return
    update_adding()


def add_prod3():
    name = combobox3.get()
    if(adddrinkqnty.get()!=""):
        quantity = int(adddrinkqnty.get())
         # Insert the new product into the database.
        try:
          cursor.execute("UPDATE products3 SET quantity = quantity + ? WHERE name = ?", [quantity, name])
          db.commit()
        except Exception as e:
          messagebox.showerror("Error", "Failed to add product: {}".format(e))
          return

        # Show a success message.
        messagebox.showinfo("Success", "Product added successfully!")

        # Clear the user input fields.
        adddrinkqnty.delete(0, END)
    elif(adddrinkDiscount.get()!=""):
        discount = float(int(adddrinkDiscount.get())/100)
        try:
          cursor.execute("UPDATE products3 SET discount = ? WHERE name = ?", [discount, name])
          cursor.execute("UPDATE products3 SET discount_price = price - (price * ? ) WHERE name = ?", [discount, name])
          db.commit()
        except Exception as e:
          messagebox.showerror("Error", "Failed to add discount: {}".format(e))
          return
        messagebox.showinfo("Success", "Discount added successfully!")
        adddrinkDiscount.delete(0, END)
    else:
      messagebox.showerror("Error", "Please enter a valid quantity.")
      return
    update_adding()

# newproducts add function
def addNewProduct():
    if (addNewProductEntry.get() == "" or addNewProductType.get() == "" or addNewProductQuntity.get() == "" or addNewProductPrice.get()==""):
        messagebox.showerror("Error","Please fill all the fields")
        clearnewProdEntry()
    else:
        if (addNewProductType.get() == "S" or addNewProductType.get() == "s"):
            details=[addNewProductEntry.get(),int(addNewProductQuntity.get()),float(addNewProductPrice.get()),float(addNewProductPrice.get()),0]
            name=addNewProductEntry.get()
            cursor.execute("INSERT INTO newproducts1 (name) VALUES(?)",(name,))
            db.commit()
            cursor.execute("INSERT INTO products1 (name, quantity, price,discount_price,discount) VALUES(?,?,?,?,?)",details)
            db.commit()
            messagebox.showinfo("Success","product Added Successfully")
            update_adding()
            update_combobox1()
            clearnewProdEntry()
        elif (addNewProductType.get() == "G" or addNewProductType.get() == "g"):
            details=[addNewProductEntry.get(),int(addNewProductQuntity.get()),float(addNewProductPrice.get()),float(addNewProductPrice.get()),0]
            name=addNewProductEntry.get()
            cursor.execute("INSERT INTO newproducts2 (name) VALUES(?)",(name,))
            db.commit()
            cursor.execute("INSERT INTO products2 (name, quantity, price,discount_price,discount) VALUES(?,?,?,?,?)",details)
            db.commit()
            messagebox.showinfo("Success","product Added Successfully")
            update_adding()
            update_combobox2()
            clearnewProdEntry()
        elif (addNewProductType.get() == "D" or addNewProductType.get() == "d"):
            details=[addNewProductEntry.get(),int(addNewProductQuntity.get()),float(addNewProductPrice.get()),float(addNewProductPrice.get()),0]
            name=addNewProductEntry.get()
            cursor.execute("INSERT INTO newproducts3 (name) VALUES(?)",(name,))
            db.commit()
            cursor.execute("INSERT INTO products3 (name, quantity, price,discount_price,discount) VALUES(?,?,?,?,?)",details)
            db.commit()
            messagebox.showinfo("Success","product Added Successfully")
            update_adding()
            update_combobox3()
            clearnewProdEntry()
            
def clearnewProdEntry():
    addNewProductEntry.delete(0,END)
    addNewProductType.delete(0,END)
    addNewProductQuntity.delete(0,END)
    addNewProductPrice.delete(0,END)

def Delete_productbtn():
    selected_row=treeview.focus()
    if selected_row:
        data=treeview.item(selected_row)
        row=data["values"]
        name=row[0]
        if row:
           cursor.execute("DELETE FROM products1 WHERE name=?",[name])
           db.commit()
           cursor.execute("DELETE FROM newproducts1 WHERE name=?",[name])
           db.commit()
           cursor.execute("DELETE FROM products2 WHERE name=?",[name])
           db.commit()
           cursor.execute("DELETE FROM newproducts2 WHERE name=?",[name])
           db.commit()
           cursor.execute("DELETE FROM products3 WHERE name=?",[name])
           db.commit()
           cursor.execute("DELETE FROM newproducts3 WHERE name=?",[name])
           db.commit()
           messagebox.showinfo("Success","Employee Deleted Successfully")
           update_adding() 
           update_combobox3()
    else:
        messagebox.showinfo("Error","Please Select a Row")
    
    
    
def get_product_quantities1():
    cursor.execute("SELECT name, quantity,price,discount_price,discount FROM products1")
    product_quantities1 = cursor.fetchall()
    return product_quantities1
def get_product_quantities2():
    cursor.execute("SELECT name, quantity,price,discount_price,discount FROM products2")
    product_quantities2 = cursor.fetchall()
    return product_quantities2
def get_product_quantities3():
    cursor.execute("SELECT name, quantity,price,discount_price,discount FROM products3")
    product_quantities3 = cursor.fetchall()
    return product_quantities3
  

def Add_Employee():
    root.withdraw()
    os.system("python Add_Employee.py")
    root.destroy()
    os._exit(0)

def back():
  root.withdraw()
  os.system("python admin_page.py")
  root.destroy()
  os._exit(0)
  
# show products name in combobox

def get_column_values( table_name, column_name):
    cursor.execute(f"SELECT {column_name} FROM {table_name}")
    column_values = [row[0] for row in cursor.fetchall()]
    return column_values

def update_combobox1():
    # Get the column values that you want to display in the combobox.
    column_values = get_column_values("products1", "name")
    combobox1.configure(values=column_values)
def update_combobox2():
    # Get the column values that you want to display in the combobox.
    column_values = get_column_values("products2", "name")
    combobox2.configure(values=column_values)
def update_combobox3():
    # Get the column values that you want to display in the combobox.
    column_values = get_column_values("products3", "name")
    combobox3.configure(values=column_values)

root = customtkinter.CTk()
root.geometry("1460x700+0+0")
root.title("Add Products")
root.resizable(False, False)


bigFram=customtkinter.CTkFrame(root,width=980,height=580)
bigFram.pack(fill='both',expand=True) 


# top fram
topMenueFram=customtkinter.CTkFrame(bigFram,width=980,height=50)
topMenueFram.pack(fill='x',side='top')
    

# top bar
backBtn=customtkinter.CTkButton(topMenueFram,text="BACK",cursor="hand2",command=back)
backBtn.place(x=10,y=20)

Add_Emplee=customtkinter.CTkButton(topMenueFram,text="Add Employee",cursor="hand2",command=Add_Employee)
Add_Emplee.place(x=200,y=20)


# content fram
bottomfram=customtkinter.CTkFrame(bigFram,width=980,height=520)
bottomfram.pack(fill='both',expand=True)

Add_productlbl=customtkinter.CTkLabel(bottomfram,text="All Product",font=("times new roman",20,"bold"))
Add_productlbl.place(x=450,y=0)

contentfrm=customtkinter.CTkFrame(bottomfram,width=590,height=600)
contentfrm.place(x=10,y=30)
# contentlbl
contentlbl=customtkinter.CTkLabel(contentfrm,text='Add_Products',font=('times new roman',20,'bold'),height=50)
contentlbl.place(x=250,y=10)

# remaingng fram
remainingFram=customtkinter.CTkFrame(bottomfram,width=400,height=500)
remainingFram.place(x=600,y=30)

 
# Subproducts fram1
stasionaryl=customtkinter.CTkFrame(contentfrm,height=280)
stasionaryl.place(x=10,y=60)
# Subproducts fram2
groceryLbl=customtkinter.CTkFrame(contentfrm,height=280)
groceryLbl.place(x=200,y=60)
# Subproducts fram3
drinkLbl=customtkinter.CTkFrame(contentfrm,height=280)
drinkLbl.place(x=400,y=60)
    

addstasionary=customtkinter.CTkLabel(stasionaryl,text="Stasionary")
addstasionary.grid(row=0,column=0)

column_values1 = get_column_values("products1","name")

combobox1 =customtkinter.CTkComboBox(stasionaryl,
                                 values=column_values1,
                                 font=("Arial", 12))
combobox1.grid(row=1, column=0,pady=10)
addstasionaryqnty=customtkinter.CTkEntry(stasionaryl,font=("Arial",15),placeholder_text="Quantity")
addstasionaryqnty.grid(row=2,column=0,pady=10)
addstasionaryDiscount=customtkinter.CTkEntry(stasionaryl,font=("Arial",15),placeholder_text="Discount %")
addstasionaryDiscount.grid(row=3,column=0,pady=10)
addstasionaryBtn=customtkinter.CTkButton(stasionaryl,text="Add",command=add_prod1)
addstasionaryBtn.grid(row=4, column=0,pady=10)
    
addgroceryLbl=customtkinter.CTkLabel(groceryLbl,text="Grocery")
addgroceryLbl.grid(row=0,column=0)

column_values2 = get_column_values("products2","name")
combobox2 =customtkinter.CTkComboBox(groceryLbl,
                                 values=column_values2,
                                 font=("Arial", 12))
combobox2.grid(row=1, column=0,pady=10)
addgroceryqnty=customtkinter.CTkEntry(groceryLbl,font=("Arial",15),placeholder_text="Quantity")
addgroceryqnty.grid(row=2,column=0,pady=10)
addgroceryDiscount=customtkinter.CTkEntry(groceryLbl,font=("Arial",15),placeholder_text="Discount %")
addgroceryDiscount.grid(row=3,column=0,pady=10)
addgroceryBtn=customtkinter.CTkButton(groceryLbl,text="Add",command=add_prod2)
addgroceryBtn.grid(row=4, column=0,pady=10)
    
adddrinkLbl=customtkinter.CTkLabel(drinkLbl,text="Drink")
adddrinkLbl.grid(row=0,column=0)

column_values3 = get_column_values("products3","name")
combobox3 =customtkinter.CTkComboBox(drinkLbl,
                                 values=column_values3,
                                 font=("Arial", 12))
combobox3.grid(row=1, column=0,pady=10)
adddrinkqnty=customtkinter.CTkEntry(drinkLbl,font=("Arial",15),placeholder_text="Quantity")
adddrinkqnty.grid(row=2,column=0,pady=10)
adddrinkDiscount=customtkinter.CTkEntry(drinkLbl,font=("Arial",15),placeholder_text="Discount %")
adddrinkDiscount.grid(row=3,column=0,pady=10)
adddrinkBtn=customtkinter.CTkButton(drinkLbl,text="Add",command=add_prod3) 
adddrinkBtn.grid(row=4, column=0,pady=10)
    
# Remaining Products
remainingLbl=customtkinter.CTkLabel(remainingFram,text="Remaining Products",font=('times new roman',20,'bold'),height=50)
remainingLbl.pack(side='top',fill='both')
     
addNewProductsLbl=customtkinter.CTkLabel(contentfrm,text="Add New Products",font=('times new roman',20,'bold'))
addNewProductsLbl.place(x=200,y=300)

addNewProductEntry=customtkinter.CTkEntry(contentfrm,font=("Arial",15),placeholder_text="Product Name")
addNewProductEntry.place(x=80,y=340)
addNewProductType=customtkinter.CTkEntry(contentfrm,font=("Arial",15),placeholder_text="Type: S/G/D")
addNewProductType.place(x=300,y=340)

addNewProductPrice=customtkinter.CTkEntry(contentfrm,font=("Arial",15),placeholder_text="Price")
addNewProductPrice.place(x=80,y=380)

addNewProductQuntity=customtkinter.CTkEntry(contentfrm,font=("Arial",15),placeholder_text="Quantity")
addNewProductQuntity.place(x=300,y=380)

addNewProductBtn1=customtkinter.CTkButton(contentfrm,text="Add",fg_color='#03a819',hover_color='#03a819',corner_radius=20,command=addNewProduct,width=500)
addNewProductBtn1.place(x=20,y=430)

addNewProductBtn3=customtkinter.CTkButton(contentfrm,text="Delete",fg_color='#cf061a',hover_color='#cf061a',corner_radius=20,command=Delete_productbtn,width=500)
addNewProductBtn3.place(x=20,y=480)



##Treeview widget data
style = ttk.Style()

# Configure the style to use a font size of 12.
style.configure("mystyle.Treeview", font=('times new roman', 14))
style.configure('mystyle.Treeview.Heading',font=('times new roman', 16,'bold'))
style.layout("mystyle.Treeview",[('mystyle.Treeview.treearea',{'sticky':'nwes'})])


table_data1=get_product_quantities1() #fatching product1
table_data2=get_product_quantities2()
table_data3=get_product_quantities3()

treeview = ttk.Treeview(remainingFram,columns=(1,2,3,4,5),show='headings',style='mystyle.Treeview',height=28,selectmode='extended')

# Add the headers to the treeview widget.
treeview["columns"] = ("Product Name", "Quantity","Price","Discount_price","Discount")
treeview.heading("Product Name", text="Product Name",)
treeview.heading("Quantity", text="Quantity")
treeview.heading("Price", text="Price")
# add two more heading
treeview.heading("Discount_price", text="Discount_price")
treeview.heading("Discount", text="Discount")
# Insert the table data into the treeview widget.
for row in table_data1:
    treeview.insert("", tk.END, values=row)
for row in table_data2:
    treeview.insert("", tk.END, values=row)
for row in table_data3:
    treeview.insert("", tk.END, values=row)

# Remove the `Product ID` column from the treeview widget.
treeview["displaycolumns"] = ("Product Name", "Quantity","Price","Discount_price","Discount")
# Set the `columnconfigure` method for the treeview widget to remove the space.
treeview.columnconfigure(0, weight=1)
treeview.columnconfigure(1, weight=1)
treeview.columnconfigure(2, weight=1)
# add two more column
treeview.columnconfigure(3, weight=1)
treeview.columnconfigure(4, weight=1)

# Pack the treeview widget.
scrollbar = ttk.Scrollbar(remainingFram, orient="vertical", command=treeview.yview)
treeview.config(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
treeview.pack(side='right',fill='both', expand=True)




root.mainloop()


