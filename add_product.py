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

def checklessproduct():
    cursor.execute("SELECT name FROM ContainerTable WHERE  quantity<10 ")
    value = cursor.fetchone()
    if value:
        messagebox.showwarning("Worning",f"The stock of {value[0]}'s is going to be ended")
    else:
        pass


def update_productbtn():
    selected_row=treeview.focus()
    if selected_row:
        data=treeview.item(selected_row)
        row=data["values"]
        if row:
           cursor.execute("UPDATE products1 set price=? WHERE name=?",(int(addNewProductPrice.get()),row[0]))
           db.commit()
           cursor.execute("UPDATE products2 set price=? WHERE name=?",(int(addNewProductPrice.get()),row[0]))
           db.commit()
           cursor.execute("UPDATE products3 set price=? WHERE name=?",(int(addNewProductPrice.get()),row[0]))
           db.commit()
           cursor.execute("UPDATE ContainerTable set price=? WHERE name=?",(int(addNewProductPrice.get()),row[0]))
           db.commit()
           messagebox.showinfo("Success","product update succesfully Successfully")
           update_adding() 
           update_combobox1()
           update_combobox2()
           update_combobox3()
           addNewProductPrice.delete(0,END)
    else:
        messagebox.showinfo("Error","Please Select a Row")


def get_quantity(name,tablename):
    try:
        cursor.execute(f"SELECT quantity FROM {tablename} WHERE name = ?", (name,))
        qunt = cursor.fetchone()[0]
        
    except Exception:
        messagebox.showerror("Error", "Spelling is not currect of the Products")
        return
    return qunt
def get_price(name,tablename):
    cursor.execute(f"SELECT price FROM {tablename} WHERE name = ?", (name,))
    price = cursor.fetchone()[0]
    return price
def get_disc(name,tablename):
    cursor.execute(f"SELECT discount FROM {tablename} WHERE name = ?", (name,))
    disc = cursor.fetchone()[0]
    return disc

def serach_products():
    if prod_name_search.get()!="":
        s_prod_name=prod_name_search.get().lower()
        search_data(s_prod_name)
        return
    else:
        messagebox.showerror("Error", "Please enter Products name.")
        return

def search_data(search_term):
    if search_term:
        cursor.execute("SELECT * FROM ContainerTable WHERE lower(name) like '%" + search_term + "%'")
    else:
        cursor.execute("SELECT * FROM ContainerTable")
    results = cursor.fetchall()

    # Clear the Treeview
    treeview.delete(*treeview.get_children())

    # Add the search results to the Treeview
    for row in results:
        treeview.insert('', 'end', values=row)

def get_data(event):
    new_clear()
    selected_row=treeview.focus()
    data=treeview.item(selected_row)
    row=data["values"]
    s_pr_name_enty.insert(0,row[0])
    s_pr_qnt_enty.insert(0,row[1])
    s_pr_price_enty.insert(0,row[2])
    s_pr_discount_enty.insert(0,row[4])


def Clear():
   prod_name_search.delete(0,END)
   s_pr_name_enty.delete(0,END)
   s_pr_qnt_enty.delete(0,END)
   s_pr_price_enty.delete(0,END)
   s_pr_discount_enty.delete(0,END)
   # Clear the Treeview
   treeview.delete(*treeview.get_children())
   cursor.execute("SELECT * FROM ContainerTable")
   results = cursor.fetchall()  
   for row in results:
        treeview.insert('', 'end', values=row)
   # Add the search results to the Treeview
   

def new_clear():
   prod_name_search.delete(0,END)
   s_pr_name_enty.delete(0,END)
   s_pr_qnt_enty.delete(0,END)
   s_pr_price_enty.delete(0,END)
   s_pr_discount_enty.delete(0,END)


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
          cursor.execute("UPDATE ContainerTable SET quantity = quantity + ? WHERE name = ?", [quantity, name])
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
          cursor.execute("UPDATE ContainerTable SET quantity = quantity + ? WHERE name = ?", [quantity, name])
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
          cursor.execute("UPDATE ContainerTable SET quantity = quantity + ? WHERE name = ?", [quantity, name])
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
          cursor.execute("UPDATE ContainerTable SET discount = ? WHERE name = ?", [discount, name])
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
            cursor.execute("INSERT INTO ContainerTable (name, quantity, price,discount_price,discount) VALUES(?,?,?,?,?)",details)
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
            cursor.execute("INSERT INTO ContainerTable (name, quantity, price,discount_price, discount) VALUES(?,?,?,?,?)",details)
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
            cursor.execute("INSERT INTO ContainerTable (name, quantity, price,discount_price,discount) VALUES(?,?,?,?,?)",details)
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
           cursor.execute("DELETE FROM ContainerTable WHERE name=?",[name])
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
root.geometry("1525x785+0+0")
root.title("Add Products")
root.resizable(False, False)


bigFram=customtkinter.CTkFrame(root,width=1450,height=780)
bigFram.pack(fill='both',expand=True) 

checklessproduct()
# top fram
topMenueFram=customtkinter.CTkFrame(bigFram,width=1450,height=50)
topMenueFram.pack(fill='x',side='top')
    

# top bar
backBtn=customtkinter.CTkButton(topMenueFram,text="BACK",cursor="hand2",command=back)
backBtn.place(x=10,y=20)

Add_Emplee=customtkinter.CTkButton(topMenueFram,text="Add Employee",cursor="hand2",command=Add_Employee)
Add_Emplee.place(x=200,y=20)


# content fram
bottomfram=customtkinter.CTkFrame(bigFram,width=1450,height=720)
bottomfram.pack(fill='both',expand=True)

Add_productlbl=customtkinter.CTkLabel(bottomfram,text="All Product",font=("times new roman",30,"bold"))
Add_productlbl.place(x=650,y=5)

contentfrm=customtkinter.CTkFrame(bottomfram,width=750,height=600)
contentfrm.place(x=10,y=50)
# contentlbl
contentlbl=customtkinter.CTkLabel(contentfrm,text='Add_Products',font=('times new roman',20,'bold'),height=50)
contentlbl.place(x=260,y=10)

# Right  fram
#serach product fram
searchfram = customtkinter.CTkFrame(bottomfram,width=820,height=200)
searchfram.place(x=650,y=50)
remainingFram=customtkinter.CTkFrame(bottomfram,width=780,height=350)
remainingFram.place(x=650,y=250)

 
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

addNewProductBtn2=customtkinter.CTkButton(contentfrm,text="Update",fg_color='#b86512',hover_color='#b86512',corner_radius=20,command=update_productbtn,width=500)
addNewProductBtn2.place(x=20,y=480)

addNewProductBtn3=customtkinter.CTkButton(contentfrm,text="Delete",fg_color='#cf061a',hover_color='#cf061a',corner_radius=20,command=Delete_productbtn,width=500)
addNewProductBtn3.place(x=20,y=530)



#product search box for checking quantity:
product_lbl=customtkinter.CTkLabel(searchfram,text="Cheack quantity of the Products",font=("Arial",15),)
product_lbl.place(x=20,y=20)
prod_name_search=customtkinter.CTkEntry(searchfram,placeholder_text='Search Products',font=("Arial",15),height=40,width=200)
prod_name_search.place(x=10,y=70)
prod_search_btn=customtkinter.CTkButton(searchfram,text='Search',font=("Arial",12),command=serach_products,height=40,width=200)
prod_search_btn.place(x=10,y=120)
prod_search_clr_btn=customtkinter.CTkButton(searchfram,text='Clear',font=("Arial",12),command=Clear,height=30,width=200,fg_color="red")
prod_search_clr_btn.place(x=10,y=170)

search_prod_detailsfrm = customtkinter.CTkFrame(searchfram,height=300,width=400)
search_prod_detailsfrm.place(x=260,y=30)
s_pr_name_lvl = customtkinter.CTkLabel(search_prod_detailsfrm,text="Product Name:",font=("Arial",15,"bold"))
s_pr_name_lvl.place(x=10,y=10)
s_pr_name_enty = customtkinter.CTkEntry(search_prod_detailsfrm,font=("Arial",15,"bold"))
s_pr_name_enty.place(x=150,y=10)


s_pr_qnt_lvl = customtkinter.CTkLabel(search_prod_detailsfrm,text="Quantity:",font=("Arial",15,"bold"))
s_pr_qnt_lvl.place(x=10,y=50)
s_pr_qnt_enty = customtkinter.CTkEntry(search_prod_detailsfrm,font=("Arial",15,"bold"))
s_pr_qnt_enty.place(x=150,y=50)


s_pr_price_lvl = customtkinter.CTkLabel(search_prod_detailsfrm,text="Product price:",font=("Arial",15,"bold"))
s_pr_price_lvl.place(x=10,y=90)
s_pr_price_enty = customtkinter.CTkEntry(search_prod_detailsfrm,font=("Arial",15,"bold"))
s_pr_price_enty.place(x=150,y=90)

s_pr_discount_lvl = customtkinter.CTkLabel(search_prod_detailsfrm,text="Discount:",font=("Arial",15,"bold"))
s_pr_discount_lvl.place(x=10,y=130)
s_pr_discount_enty = customtkinter.CTkEntry(search_prod_detailsfrm,font=("Arial",15,"bold"))
s_pr_discount_enty.place(x=150,y=130)

##Treeview widget data
style = ttk.Style()

# Configure the style to use a font size of 12.
style.configure("mystyle.Treeview", font=('times new roman', 14))
style.configure('mystyle.Treeview.Heading',font=('times new roman', 16,'bold'))
style.layout("mystyle.Treeview",[('mystyle.Treeview.treearea',{'sticky':'nwes'})])


table_data1=get_product_quantities1() #fatching product1
table_data2=get_product_quantities2()
table_data3=get_product_quantities3()

treeview = ttk.Treeview(remainingFram,columns=(1,2,3,4,5),show='headings',style='mystyle.Treeview',height=20,selectmode='extended')

treeview.heading('1',text='Product Name')
treeview.column('1',width=200)
treeview.heading('2',text='Quantity')
treeview.column('2',width=150)
treeview.heading('3',text='Price')
treeview.column('3',width=150)
treeview.heading('4',text='Discount_price')
treeview.column('4',width=150)
treeview.heading('5',text='Discount')
treeview.column('5',width=150)
treeview.bind('<ButtonRelease-1>',get_data)

for row in table_data1:
    treeview.insert("", tk.END, values=row)
for row in table_data2:
    treeview.insert("", tk.END, values=row)
for row in table_data3:
    treeview.insert("", tk.END, values=row)

# Pack the treeview widget.
scrollbar = ttk.Scrollbar(remainingFram, orient="vertical", command=treeview.yview)
treeview.config(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
treeview.pack(side='right',fill='both', expand=True)




root.mainloop()


