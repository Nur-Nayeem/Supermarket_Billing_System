from tkinter import *
from tkinter import messagebox
import sqlite3
import random
import os,tempfile
import customtkinter
import re
import time
from PIL import Image, ImageTk
import datetime


# database
db=sqlite3.connect('supermarket.db')
cursor=db.cursor()

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")
# functions:

def valid_quantity(tablename,name,quantity):
    cursor.execute(f"SELECT quantity FROM {tablename} WHERE name = ?", (name,))
    value = cursor.fetchone()[0]
    qnt=int(quantity)
    try:
        if qnt > value:
            messagebox.showerror("Error", "Not enough quantity of product")
            quantity='0'
    except Exception as e:
        messagebox.showerror("Error", "Failed to add product: {}".format(e))
    return quantity

def get_column_values( table_name, column_name):
    cursor.execute(f"SELECT {column_name} FROM {table_name}")
    column_values = [row[0] for row in cursor.fetchall()]
    return column_values


#exit function
def exit():
    exit = messagebox.askyesno("Exit", "Are you sure you want to exit?")
    if exit:
        window.destroy()
        os._exit(0)

#save function
def save():
    with open("data.txt","w") as f:
        f.write(str(prod1qnty.get()))
        f.write("\n")
        f.write(str(prod2qnty.get()))
        f.write("\n")

#clear function
def clear():
    bilArea.configure(billfram,state='normal')
    prod1qnty.delete(0,END)
    prod2qnty.delete(0,END)
    prod3qnty.delete(0,END)
    prod4qnty.delete(0,END)
    prod5qnty.delete(0,END)
    prod6qnty.delete(0,END)
    combobox1qntty.delete(0,END)
    gros1qnty.delete(0,END)
    gros2qnty.delete(0,END)
    gros3qnty.delete(0,END)
    gros4qnty.delete(0,END)
    gros5qnty.delete(0,END)
    gros6qnty.delete(0,END)
    combobox2qntty.delete(0,END)
    drink1qnty.delete(0,END)
    drink2qnty.delete(0,END)
    drink3qnty.delete(0,END)
    drink4qnty.delete(0,END)
    drink5qnty.delete(0,END)
    drink6qnty.delete(0,END)
    combobox3qntty.delete(0,END)
    bilArea.delete('1.0',END)
    stasionarypriceentry.delete(0,END)
    grocerypriceentry.delete(0,END)
    drinkpriceentry.delete(0,END)
    stasionaryTaxentry.delete(0,END)
    groceryTaxentry.delete(0,END)
    drinkTaxentry.delete(0,END)
    total_priceentry.delete(0,END)
    disc_entry.delete(0,END)
    nameEntery.delete(0,END)
    phonEntery.delete(0,END)
    emailEntery.delete(0,END)
    billNoEntery.delete(0,END)

    
    
    

#print bill function
def print_bill():
    if bilArea.get('1.0',END)=='\n':
        messagebox.showerror("Error","Bill is empty")
    else:
        file=tempfile.mktemp('.txt')
        open(file,'w').write(bilArea.get('1.0',END))
        os.startfile(file,'print')

#search bill
def search_bill():
    for i in os.listdir('bills/'):
        if i.split('.')[0]==billNoEntery.get():
            f=open(f'bills/{i}','r')
            bilArea.delete(1.0,END)
            for data in f:
                bilArea.insert(END,data)
            f.close()
            break
    else:
        messagebox.showerror("Error","Bill not found")
    bilArea.configure(billfram,state='disabled')
# bill_save
if not os.path.exists("bills"):
    os.mkdir("bills")

def bill_save():
    global billnum
    save=messagebox.askyesno("Confirm","Do you want to save the bill?")
    if save:
        bill_content=bilArea.get(1.0,END)
        file=open(f"bills/{billnum}.txt","w")
        file.write(bill_content)
        file.close()
        messagebox.showinfo("Success",f"Bill number {billnum} is Saved Successfully")
        billnum=random.randint(1000,9999)
        return True


# getting original price from products table in database
def get_price(name,tablename):
    cursor.execute(f"SELECT price FROM {tablename} WHERE name = ?", (name,))
    price = cursor.fetchone()[0]
    return price

#getting discount price from database
def get_disc_price(name,tablename):
    cursor.execute(f"SELECT discount_price FROM {tablename} WHERE name = ?", (name,))
    disc_price = cursor.fetchone()[0]
    return disc_price


def billEachprod(tablename,name,quantity,price):
    cursor.execute(f"SELECT quantity FROM {tablename} WHERE name = ?", (name,))
    value = cursor.fetchone()[0]
    try:
        if quantity <= value:
            cursor.execute(f"UPDATE {tablename} SET quantity = quantity - ? WHERE name = ?", [quantity, name])
            db.commit()
            bilArea.insert(END,f"\n{name}  \t\t\t\t  {quantity}\t\t\t\t{price} TK")
        else:
            messagebox.showerror("Error", "gh quantity of product")
            return
    except Exception as e:
      messagebox.showerror("Error", "Failed to add product: {}".format(e))

def alsoupdate(tablename,name,quantity):
    cursor.execute(f"SELECT quantity FROM {tablename} WHERE name = ?", (name,))
    value = cursor.fetchone()[0]
    try:
        if quantity <= value:
            cursor.execute(f"UPDATE {tablename} SET quantity = quantity - ? WHERE name = ?", [quantity, name])
            db.commit()
        else:
            messagebox.showerror("Error", "Not enough quantity of product")
            return
    except Exception as e:
      messagebox.showerror("Error", "Failed to add product: {}".format(e))              

def addCmbItem1():
    name=combobox1.get()
    quantity=int(combobox1qntty.get())
    combo_dict[name] = quantity
    pr1=int(valid_quantity("products1",name,combobox1qntty.get()))
    price1 = (pricecomboboxproduct(combobox1,"products1")*pr1)
    discprice1= (priceDisccomboboxproduct(combobox1,"products1") *pr1)
    comblistPrice.append(price1)
    comblistDiscPrice.append(discprice1)
    combobox1qntty.delete(0,END)
def addCmbItem2():
    name=combobox2.get()
    quantity=int(combobox2qntty.get())
    combo_dict2[name] = quantity
    pr2=int(valid_quantity("products2",name,combobox2qntty.get()))
    price = (pricecomboboxproduct(combobox2,"products2")*pr2)
    discprice= (priceDisccomboboxproduct(combobox2,"products2") * pr2)
    comblistPrice2.append(price)
    comblistDiscPrice2.append(discprice)
    combobox2qntty.delete(0,END)
def addCmbItem3():
    name=combobox3.get()
    quantity=int(combobox3qntty.get())
    combo_dict3[name] = quantity
    pr3=int(valid_quantity("products3",name,combobox3qntty.get()))
    price = (pricecomboboxproduct(combobox3,"products3")*pr3)
    discprice= (priceDisccomboboxproduct(combobox3,"products3") * pr3)
    comblistPrice3.append(price)
    comblistDiscPrice3.append(discprice)
    combobox3qntty.delete(0,END)
    
    


billnum=random.randint(1000,9999)
def bill_area():
    bilArea.delete(1.0,END)
    reg_name= r"^[a-zA-Z]{3,}$"
    reg_exp = r"^01\d{9}$"
    email_regex = r"^[^@]+@[^@]+\.[^@]+$"
    if nameEntery.get()=="" or phonEntery.get()=="" or emailEntery.get()=="":
        messagebox.showerror("Error","Please fill the Customer Details")
    elif stasionarypriceentry.get()=="" or grocerypriceentry.get()=="" or drinkpriceentry.get()=="":
        messagebox.showerror("Error","No Product are selected")
    elif stasionarypriceentry.get()=="0 TK" and grocerypriceentry.get()=="0 TK" and drinkpriceentry.get()=="0 TK":
        messagebox.showerror("Error","No Product are selected")
    else:
        if not re.match(reg_name, nameEntery.get()):
           messagebox.showerror("Error","Name is not valid")
           return
        if not re.match(reg_exp, phonEntery.get()):
           messagebox.showerror("Error","Phone Number is not valid")
           return
        if not re.match(email_regex, emailEntery.get()):
           messagebox.showerror("Error","Email is not valid")
           return
        bilArea.insert(END,"\t\t\t     ****Welcome Customer****\n\n")
        bilArea.insert(END,f"Bill Number:        {billnum}   \t\t\t\t\t Date: {time.ctime(time.time())}")
        bilArea.insert(END,f"\nCustomer Name:  {nameEntery.get()}")
        bilArea.insert(END,f"\nPhone Number:    {phonEntery.get()}")
        bilArea.insert(END,f"\nEmail       :    {emailEntery.get()}")
        bilArea.insert(END,"\n================================================================")
        bilArea.insert(END,"\nProducts\t\t\t\tQuantity\t\t\t\tPrices")
        bilArea.insert(END,"\n================================================================")
        # stasionary bill
        if prod1qnty.get()!='0':
            name = 'Face Creem'
            quantity = int(prod1qnty.get())
            price= get_price(name,"products1")*quantity
            billEachprod("products1",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
        if prod2qnty.get()!='0':
            name = 'Bath Soup'
            quantity = int(prod2qnty.get())
            price= get_price(name,"products1")*quantity
            billEachprod("products1",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
              
        if prod3qnty.get()!='0':
            name = 'Face Wash'
            quantity = int(prod3qnty.get())
            price= get_price(name,"products1")*quantity
            billEachprod("products1",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
        if prod4qnty.get()!='0':
            name = 'Tooth Pest'
            quantity = int(prod4qnty.get())
            price= get_price(name,"products1")*quantity
            billEachprod("products1",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
        if prod5qnty.get()!='0':
            name = 'Hair Gel'
            quantity = int(prod5qnty.get())
            price= get_price(name,"products1")*quantity
            billEachprod("products1",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
        if prod6qnty.get()!='0':
            name = 'Body Lousion'
            quantity = int(prod6qnty.get())
            price= get_price(name,"products1")*quantity
            billEachprod("products1",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
        if len(combo_dict)!=0:
            i=0
            for key, value in combo_dict.items():
                name=key
                quantity=value
                price=comblistPrice[i]
                i=i+1; 
                billEachprod("products1",name,quantity,price)   
                alsoupdate("ContainerTable",name,quantity)         
            
     
        # grocery bill
        if gros1qnty.get()!='0':
            name = 'Rice'
            quantity = int(gros1qnty.get())
            price= get_price(name,"products2")*quantity
            billEachprod("products2",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
        if gros2qnty.get()!='0':
            name = 'Oil'
            quantity = int(gros2qnty.get())
            price= get_price(name,"products2")*quantity
            billEachprod("products2",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
        if gros3qnty.get()!='0':
            name = 'Suger'
            quantity = int(gros3qnty.get())
            price= get_price(name,"products2")*quantity
            billEachprod("products2",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
        if gros4qnty.get()!='0':
            name = 'Dall'
            quantity = int(gros4qnty.get())
            price= get_price(name,"products2")*quantity
            billEachprod("products2",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
        if gros5qnty.get()!='0':
            name = 'Tea'
            quantity = int(gros5qnty.get())
            price= get_price(name,"products2")*quantity
            billEachprod("products2",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
        if gros6qnty.get()!='0':
            name = 'Bread'
            quantity = int(gros6qnty.get())
            price= get_price(name,"products2")*quantity
            billEachprod("products2",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
        
        if len(combo_dict2)!=0:
            i=0
            for key, value in combo_dict2.items():
                name=key
                quantity=value
                price=comblistPrice2[i]
                i=i+1; 
                billEachprod("products2",name,quantity,price)
                alsoupdate("ContainerTable",name,quantity)
        
        # Drinks bill
        if drink1qnty.get()!='0':
            name = 'Milk'
            quantity = int(drink1qnty.get())
            price= get_price(name,"products3")*quantity
            billEachprod("products3",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
        if drink2qnty.get()!='0':
            name = 'Pepsi'
            quantity = int(drink2qnty.get())
            price= get_price(name,"products3")*quantity
            billEachprod("products3",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
        if drink3qnty.get()!='0':
            name = '7 Up'
            quantity = int(drink3qnty.get())
            price= get_price(name,"products3")*quantity
            billEachprod("products3",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
        if drink4qnty.get()!='0':
            name = 'Coca Cola'
            quantity = int(drink4qnty.get())
            price= get_price(name,"products3")*quantity
            billEachprod("products3",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
        if drink5qnty.get()!='0':
            name = 'Speed'
            quantity = int(drink5qnty.get())
            price= get_price(name,"products3")*quantity
            billEachprod("products3",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
        if drink6qnty.get()!='0':
            name = 'Sprite'
            quantity = int(drink6qnty.get())
            price= get_price(name,"products3")*quantity
            billEachprod("products3",name,quantity,price)
            alsoupdate("ContainerTable",name,quantity)
            
        if len(combo_dict3)!=0:
            i=0
            for key, value in combo_dict3.items():
                name=key
                quantity=value
                price=comblistPrice3[i]
                i=i+1; 
                billEachprod("products3",name,quantity,price)
                alsoupdate("ContainerTable",name,quantity)
        
        bilArea.insert(END,"\n----------------------------------------------------------------------------------------------------------------")
        if stasionaryTaxentry.get()!='0.0 TK':
            bilArea.insert(END,f"\nStationary Tax\t\t\t\t\t\t\t\t{round(stasionarytaxPrice,8)} TK")
        if groceryTaxentry.get()!='0.0 TK':
            bilArea.insert(END,f"\nGrocery Tax\t\t\t\t\t\t\t\t{round(grocerytaxPrice,8)} TK")
        if drinkTaxentry.get()!='0.0 TK':
            bilArea.insert(END,f"\nDrink Tax\t\t\t\t\t\t\t\t{round(drinksstaxPrice,8)} TK")
        bilArea.insert(END,"\n---------------------------------------------------------------------------------------------------------------")
        bilArea.insert(END,f"\nTotal: \t\t\t\t\t\t\t\t{round(totalPriceWithTax,8)} TK")
        bilArea.insert(END,f"\nDiscount\t\t\t\t\t\t\t\t{round(discounts,8)} TK")
        bilArea.insert(END,"\n---------------------------------------------------------------------------------------------------------------")
        bilArea.insert(END,f"\nTotal Bill\t\t\t\t\t\t\t\t{round(totalAfterDiscount,8)} TK")
        newnum=billnum
        if bill_save():
            cursor.execute("INSERT INTO customers(Billid,Name,Mobile,Mail,Total_Sell,Time) VALUES(?,?,?,?,?,?)",(newnum,nameEntery.get(),phonEntery.get(),emailEntery.get(),round(totalAfterDiscount,8),time.ctime(time.time())))
            db.commit()
        bilArea.configure(billfram,state='disabled')
        
        



def pricecomboboxproduct(combobox,tablename):
    name = combobox.get()
    cursor.execute(f"SELECT price FROM {tablename} WHERE name = ?", (name,))
    price = cursor.fetchone()[0]
    return price
def priceDisccomboboxproduct(combobox,tablename):
    name = combobox.get()
    cursor.execute(f"SELECT discount_price FROM {tablename} WHERE name = ?", (name,))
    disc_price = cursor.fetchone()[0]
    return disc_price

def checklessproduct():
    cursor.execute("SELECT name FROM ContainerTable WHERE  quantity<10 ")
    value = cursor.fetchone()
    if value:
        messagebox.showwarning("Worning",f"The stock of {value[0]}'s is going to be ended")
    else:
        pass


def total():
    #stasionary total price
    global fcrmPrice,bathSopPice,facewasPrice,thpestPrice,hairGelPrice,bodyLosonPrice,\
    fcrmDiscPrice,bathSopDiscPrice,facewasDiscPrice,thpestDiscPrice,hairGelDiscPrice,bodyLosonDiscPrice,\
    ricePrice,oilPrice,sugerPrice,dallPrice,teaPrice,breadPrice,\
    riceDiscPrice,oilDiscPrice,sugerDiscPrice,dallDiscPrice,teaDiscPrice,breadDiscPrice,\
    milkPrice,pepsiPrice,sevenUpPrice,cocPrice,speedPrice,spritePrice,\
    milkDiscPrice,pepsiDiscPrice,sevenUpDiscPrice,cocDiscPrice,speedDiscPrice,spriteDiscPrice,\
    stasionarytaxPrice,grocerytaxPrice,drinksstaxPrice,\
    newProdcomboboxPrice1,newProdcomboboxTprice1,newProdcomboboxPrice2,\
    newProdcomboboxTprice2,newProdcomboboxPrice3,newProdcomboboxTprice3,totalPriceWithTax,\
    newProdcomboboxDiscPrice1,newProdcomboboxTotalDiscprice1,total_disc_StationaryPrice,newProdcomboboxDiscPrice2,\
    newProdcomboboxTotalDiscprice2,totalGroceryDiscountPrice,newProdcomboboxDiscPrice3,newProdcomboboxTotalDiscprice3,\
    totalDiscDrinkPrice,total_discount_price,total_price_withoutTax,discounts,totalAfterDiscount
    
    newProdcomboboxPrice1=0
    newProdcomboboxDiscPrice1=0
    newProdcomboboxPrice2=0
    newProdcomboboxDiscPrice2=0
    newProdcomboboxPrice3=0
    newProdcomboboxDiscPrice3=0
    
    if (prod1qnty.get()==""): 
        prod1qnty.insert(0,0)
    if (prod2qnty.get()==""): 
        prod2qnty.insert(0,0)
    if (prod3qnty.get()==""): 
        prod3qnty.insert(0,0)
    if (prod4qnty.get()==""): 
        prod4qnty.insert(0,0)
    if (prod5qnty.get()==""): 
        prod5qnty.insert(0,0)
    if (prod6qnty.get()==""): 
        prod6qnty.insert(0,0)
    if (combobox1qntty.get()==""): 
        combobox1qntty.insert(0,0)
    if (gros1qnty.get()==""): 
        gros1qnty.insert(0,0)
    if (gros2qnty.get()==""): 
        gros2qnty.insert(0,0)
    if (gros3qnty.get()==""): 
        gros3qnty.insert(0,0)
    if (gros4qnty.get()==""): 
        gros4qnty.insert(0,0)
    if (gros5qnty.get()==""): 
        gros5qnty.insert(0,0)
    if (gros6qnty.get()==""): 
        gros6qnty.insert(0,0)
    if (combobox2qntty.get()==""): 
        combobox2qntty.insert(0,0)
    if (drink1qnty.get()==""): 
        drink1qnty.insert(0,0)
    if (drink2qnty.get()==""): 
        drink2qnty.insert(0,0)
    if (drink3qnty.get()==""): 
        drink3qnty.insert(0,0)
    if (drink4qnty.get()==""): 
        drink4qnty.insert(0,0)
    if (drink5qnty.get()==""): 
        drink5qnty.insert(0,0)
    if (drink6qnty.get()==""): 
        drink6qnty.insert(0,0)
    if (combobox3qntty.get()==""): 
        combobox3qntty.insert(0,0)
        
    if combobox1qntty.get()!='0':
        addCmbItem1()
        
    if combobox2qntty.get()!='0':
        addCmbItem2()
        
    if combobox3qntty.get()!='0':
        addCmbItem3()
        
    fcq=int(valid_quantity("products1","Face Creem",prod1qnty.get()))
    fcrmPrice=fcq*get_price("Face Creem","products1")
    fcrmDiscPrice=fcq*get_disc_price("Face Creem","products1")
    bcq=int(valid_quantity("products1","Bath Soup",prod2qnty.get()))
    bathSopPice=bcq*get_price("Bath Soup","products1")
    bathSopDiscPrice=bcq*get_disc_price("Bath Soup","products1")
    fcw=int(valid_quantity("products1","Face Wash",prod3qnty.get()))
    facewasPrice=fcw*get_price("Face Wash","products1")
    facewasDiscPrice=fcw*get_disc_price("Face Wash","products1")
    thpst=int(valid_quantity("products1","Tooth Pest",prod4qnty.get()))
    thpestPrice=thpst*get_price("Tooth Pest","products1")
    thpestDiscPrice=thpst*get_disc_price("Tooth Pest","products1")
    hrgl=int(valid_quantity("products1","Hair Gel",prod5qnty.get()))
    hairGelPrice=hrgl*get_price("Hair Gel","products1")
    hairGelDiscPrice=hrgl*get_disc_price("Hair Gel","products1")
    bdlsn=int(valid_quantity("products1","Body Lousion",prod6qnty.get()))
    bodyLosonPrice=bdlsn*get_price("Body Lousion","products1")
    bodyLosonDiscPrice=bdlsn*get_disc_price("Body Lousion","products1")
    
    for item in comblistPrice:
        newProdcomboboxPrice1 += item
    for item in comblistDiscPrice:
        newProdcomboboxDiscPrice1 += item
    newProdcomboboxTprice1=newProdcomboboxPrice1
    newProdcomboboxTotalDiscprice1=newProdcomboboxDiscPrice1
    
    
    
    totalStasionaryPrice=fcrmPrice+bathSopPice+facewasPrice+thpestPrice+hairGelPrice+bodyLosonPrice+newProdcomboboxTprice1
    total_disc_StationaryPrice=fcrmDiscPrice+bathSopDiscPrice+facewasDiscPrice+thpestDiscPrice+hairGelDiscPrice+bodyLosonDiscPrice+newProdcomboboxTotalDiscprice1
    stasionarypriceentry.delete(0,END)
    stasionarypriceentry.insert(0,str(totalStasionaryPrice) +' TK')
    
    # stasionary tax 
    stasionarytaxPrice=totalStasionaryPrice*0.05
    stasionaryTaxentry.delete(0,END)
    stasionaryTaxentry.insert(0,str(round(stasionarytaxPrice,5))+' TK')
    
    
    # grocery total price
    rcq=int(valid_quantity("products2","Rice",gros1qnty.get()))
    ricePrice=rcq*get_price("Rice","products2")
    riceDiscPrice=rcq*get_disc_price("Rice","products2")
    olq=int(valid_quantity("products2","Oil",gros1qnty.get()))
    oilPrice=olq*get_price("Oil","products2")
    oilDiscPrice=olq*get_disc_price("Oil","products2")
    sgq=int(valid_quantity("products2","Suger",gros3qnty.get()))
    sugerPrice=sgq*get_price("Suger","products2")
    sugerDiscPrice=sgq*get_disc_price("Suger","products2")
    dlq=int(valid_quantity("products2","Dall",gros4qnty.get()))
    dallPrice=dlq*get_price("Dall","products2")
    dallDiscPrice=dlq*get_disc_price("Dall","products2")
    tq=int(valid_quantity("products2","Tea",gros5qnty.get()))
    teaPrice=tq*get_price("Tea","products2")
    teaDiscPrice=tq*get_disc_price("Tea","products2")
    brq=int(valid_quantity("products2","Bread",gros6qnty.get()))
    breadPrice=brq*get_price("Bread","products2")
    breadDiscPrice=brq*get_disc_price("Bread","products2")
    
    for item in comblistPrice2:
        newProdcomboboxPrice2 += item
    for item in comblistDiscPrice2:
        newProdcomboboxDiscPrice2 += item
    newProdcomboboxTprice2=newProdcomboboxPrice2
    newProdcomboboxTotalDiscprice2=newProdcomboboxDiscPrice2
    
    
    totalGroceryPrice=ricePrice+oilPrice+sugerPrice+dallPrice+teaPrice+breadPrice+newProdcomboboxTprice2
    totalGroceryDiscountPrice=riceDiscPrice+oilDiscPrice+sugerDiscPrice+dallDiscPrice+teaDiscPrice+breadDiscPrice+newProdcomboboxTotalDiscprice2
    grocerypriceentry.delete(0,END)
    grocerypriceentry.insert(0,str(totalGroceryPrice) +' TK')
    
    # grocery tax 
    grocerytaxPrice=totalGroceryPrice*0.04
    groceryTaxentry.delete(0,END)
    groceryTaxentry.insert(0,str(round(grocerytaxPrice,5))+ ' TK')
    
    # Drinks total price
    mlkq=int(valid_quantity("products3","Milk",drink1qnty.get()))
    milkPrice=mlkq*get_price("Milk","products3")
    milkDiscPrice=mlkq*get_disc_price("Milk","products3")
    ppq=int(valid_quantity("products3","Pepsi",drink2qnty.get()))
    pepsiPrice=ppq*get_price("Pepsi","products3")
    pepsiDiscPrice=ppq*get_disc_price("Pepsi","products3")
    svnq=int(valid_quantity("products3","7 Up",drink3qnty.get()))
    sevenUpPrice=svnq*get_price("7 Up","products3")
    sevenUpDiscPrice=svnq*get_disc_price("7 Up","products3")
    ccq=int(valid_quantity("products3","Coca Cola",drink4qnty.get()))
    cocPrice=ccq*get_price("Coca Cola","products3")
    cocDiscPrice=ccq*get_disc_price("Coca Cola","products3")
    spq=int(valid_quantity("products3","Speed",drink5qnty.get()))
    speedPrice=spq*get_price("Speed","products3")
    speedDiscPrice=spq*get_disc_price("Speed","products3")
    sprq=int(valid_quantity("products3","Sprite",drink6qnty.get()))
    spritePrice=sprq*get_price("Sprite","products3")
    spriteDiscPrice=sprq*get_disc_price("Sprite","products3")
    
    for item in comblistPrice3:
        newProdcomboboxPrice3 += item
    for item in comblistDiscPrice3:
        newProdcomboboxDiscPrice3 += item
    newProdcomboboxTprice3=newProdcomboboxPrice3
    newProdcomboboxTotalDiscprice3=newProdcomboboxDiscPrice3
    
    
    
    totalDrinkPrice=milkPrice+pepsiPrice+sevenUpPrice+cocPrice+speedPrice+spritePrice+newProdcomboboxTprice3
    totalDiscDrinkPrice=milkDiscPrice+pepsiDiscPrice+sevenUpDiscPrice+cocDiscPrice+speedDiscPrice+spriteDiscPrice+newProdcomboboxTotalDiscprice3
    drinkpriceentry.delete(0,END)
    drinkpriceentry.insert(0,str(totalDrinkPrice)+ ' TK')
    
    # drink tax
     
    drinksstaxPrice=totalDrinkPrice*0.03
    drinkTaxentry.delete(0,END)
    drinkTaxentry.insert(0,str(round(drinksstaxPrice,8))+ ' TK')
    
    total_price_withoutTax=totalStasionaryPrice+totalGroceryPrice+totalDrinkPrice
    
    # total discount
    total_discount_price=total_disc_StationaryPrice+totalGroceryDiscountPrice+totalDiscDrinkPrice
    discounts=total_price_withoutTax-total_discount_price
    disc_entry.delete(0,END)
    disc_entry.insert(0,str(round(discounts,5))+ ' TK')
    
    # total price with tax
    totalPriceWithTax=totalStasionaryPrice+stasionarytaxPrice+totalGroceryPrice+grocerytaxPrice+totalDrinkPrice+drinksstaxPrice
    total_priceentry.delete(0,END)
    total_priceentry.insert(0,str(round(totalPriceWithTax,5))+ ' TK')
    
    # afterDiscount
    totalAfterDiscount=totalPriceWithTax-discounts
    
    
    
    
def back_to_Front():
      window.withdraw()
      os.system("python front.py")
      window.destroy()
      os._exit(0)

# UI Design
window=customtkinter.CTk()
window.title("Super Market Billing System")
window.geometry("1600x900+0+0")
# window.iconbitmap('icon.ico')

titleLbl=customtkinter.CTkLabel(window,text="Super Market Billing System", font=("Arial",20,"bold"))
titleLbl.pack(fill='x')

bigFram=customtkinter.CTkFrame(window,width=1200,height=700)
bigFram.pack(fill='both',expand=True) 
checklessproduct()
# Sidebar
sideMenueFram=customtkinter.CTkFrame(bigFram)
sideMenueFram.grid(row=0,column=0,rowspan=3,sticky='nws')
sideContet=customtkinter.CTkFrame(sideMenueFram,width=100,height=755)
sideContet.pack()

img1 = customtkinter.CTkImage(Image.open("backBtn.png"),size=(60,60))
backsidebtn=customtkinter.CTkButton(sideContet,text='',image=img1,fg_color='#ffffff',hover_color='#ffffff',corner_radius=50,command=back_to_Front,width=50)
backsidebtn.pack(side=TOP)



# productslbl
prodlblfrm=customtkinter.CTkLabel(bigFram,text='Products',font=('times new roman',30,'bold'))
prodlblfrm.grid(row=0,column=1,ipadx=10,padx=10,sticky='news')



# Products Frame
productFram=customtkinter.CTkFrame(bigFram)
productFram.grid(row=1,column=1,ipady=10,ipadx=10,padx=10,pady=10,sticky='new')

# Customer Details & BILL Frame
customer_dts_Bill=customtkinter.CTkFrame(bigFram)
customer_dts_Bill.grid(row=0,column=2,rowspan=2,ipady=10,ipadx=10,padx=10,pady=10,sticky='ne')


# Subproducts fram1

cosmeTicsLbl=customtkinter.CTkFrame(productFram)
cosmeTicsLbl.grid(row=0,column=0,padx=10,pady=10)

# Subproducts fram2
groceryLbl=customtkinter.CTkFrame(productFram)
groceryLbl.grid(row=0,column=1,padx=10,pady=10)

# Subproducts fram3
drinkLbl=customtkinter.CTkFrame(productFram)
drinkLbl.grid(row=0,column=2,padx=10,pady=10)

# # Stasionary Products

prod=customtkinter.CTkLabel(cosmeTicsLbl,text="Stationary",font=("Arial",20,"bold"))
prod.grid(row=0,column=0,columnspan=2,padx=10,pady=10,sticky='ew')

prod1=customtkinter.CTkLabel(cosmeTicsLbl,text="Face Cream",font=("Arial",15,"bold"))
prod1.grid(row=1,column=0,padx=10,pady=10)
prod1qnty=customtkinter.CTkEntry(cosmeTicsLbl,font=("Arial",15))
prod1qnty.grid(row=1,column=1)

prod2=customtkinter.CTkLabel(cosmeTicsLbl,text="Bath Sop",font=("Arial",15,"bold"))
prod2.grid(row=2,column=0,padx=10,pady=10)
prod2qnty=customtkinter.CTkEntry(cosmeTicsLbl,font=("Arial",15))
prod2qnty.grid(row=2,column=1)

prod3=customtkinter.CTkLabel(cosmeTicsLbl,text="Face Wash",font=("Arial",15,"bold"))
prod3.grid(row=3,column=0,padx=10,pady=10)
prod3qnty=customtkinter.CTkEntry(cosmeTicsLbl,font=("Arial",15))
prod3qnty.grid(row=3,column=1)

prod4=customtkinter.CTkLabel(cosmeTicsLbl,text="Tooth Pest",font=("Arial",15,"bold"))
prod4.grid(row=4,column=0,padx=10,pady=10)
prod4qnty=customtkinter.CTkEntry(cosmeTicsLbl,font=("Arial",15))
prod4qnty.grid(row=4,column=1)

prod5=customtkinter.CTkLabel(cosmeTicsLbl,text="Hair Gel",font=("Arial",15,"bold"))
prod5.grid(row=5,column=0,padx=10,pady=10)
prod5qnty=customtkinter.CTkEntry(cosmeTicsLbl,font=("Arial",15))
prod5qnty.grid(row=5,column=1)

prod6=customtkinter.CTkLabel(cosmeTicsLbl,text="Body Lousion",font=("Arial",15,"bold"))
prod6.grid(row=6,column=0,padx=10,pady=10)
prod6qnty=customtkinter.CTkEntry(cosmeTicsLbl,font=("Arial",15))
prod6qnty.grid(row=6,column=1)

column_values1 = get_column_values("newproducts1","name")
combobox1 =customtkinter.CTkComboBox(cosmeTicsLbl,
                                 values=column_values1,
                                 font=("Arial", 12),width=100)
combobox1.grid(row=7, column=0,padx=5,pady=5)
combobox1qntty=customtkinter.CTkEntry(cosmeTicsLbl,font=("Arial",15),width=100)
combobox1qntty.grid(row=7,column=1)
combobox1btn=customtkinter.CTkButton(cosmeTicsLbl,text="Add",width=50,command=addCmbItem1)
combobox1btn.grid(row=7,column=2)

combo_dict = {}
comblistPrice = []
comblistDiscPrice = []



# # Grocery Products

gros=customtkinter.CTkLabel(groceryLbl,text="Grocery",font=("Arial",20,"bold"))
gros.grid(row=0,column=0,columnspan=2,padx=10,pady=10,sticky='ew')

gros1=customtkinter.CTkLabel(groceryLbl,text="Rice",font=("Arial",15,"bold"))
gros1.grid(row=1,column=0,padx=10,pady=10)
gros1qnty=customtkinter.CTkEntry(groceryLbl,font=("Arial",15))
gros1qnty.grid(row=1,column=1)

gros2=customtkinter.CTkLabel(groceryLbl,text="Oil",font=("Arial",15,"bold"))
gros2.grid(row=2,column=0,padx=10,pady=10)
gros2qnty=customtkinter.CTkEntry(groceryLbl,font=("Arial",15))
gros2qnty.grid(row=2,column=1)

gros3=customtkinter.CTkLabel(groceryLbl,text="Suger",font=("Arial",15,"bold"))
gros3.grid(row=3,column=0,padx=10,pady=10)
gros3qnty=customtkinter.CTkEntry(groceryLbl,font=("Arial",15))
gros3qnty.grid(row=3,column=1)

gros4=customtkinter.CTkLabel(groceryLbl,text="Daal",font=("Arial",15,"bold"))
gros4.grid(row=4,column=0,padx=10,pady=10)
gros4qnty=customtkinter.CTkEntry(groceryLbl,font=("Arial",15))
gros4qnty.grid(row=4,column=1)

gros5=customtkinter.CTkLabel(groceryLbl,text="Tea",font=("Arial",15,"bold"))
gros5.grid(row=5,column=0,padx=10,pady=10)
gros5qnty=customtkinter.CTkEntry(groceryLbl,font=("Arial",15))
gros5qnty.grid(row=5,column=1)

gros6=customtkinter.CTkLabel(groceryLbl,text="Bread",font=("Arial",15,"bold"))
gros6.grid(row=6,column=0,padx=10,pady=10)
gros6qnty=customtkinter.CTkEntry(groceryLbl,font=("Arial",15))
gros6qnty.grid(row=6,column=1)

column_values2 = get_column_values("newproducts2","name")
combobox2 =customtkinter.CTkComboBox(groceryLbl,
                                 values=column_values2,
                                 font=("Arial", 12),width=100)
combobox2.grid(row=7, column=0,padx=10,pady=10)
combobox2qntty=customtkinter.CTkEntry(groceryLbl,font=("Arial",15),width=100)
combobox2qntty.grid(row=7,column=1)
combobox2btn=customtkinter.CTkButton(groceryLbl,text="Add",width=50,command=addCmbItem2)
combobox2btn.grid(row=7,column=2)

combo_dict2 = {}
comblistPrice2 = []
comblistDiscPrice2 = []


# # Drink Products

drink=customtkinter.CTkLabel(drinkLbl,text="Drinks",font=("Arial",20,"bold"))
drink.grid(row=0,column=0,columnspan=2,padx=10,pady=10,sticky='ew')

drink1=customtkinter.CTkLabel(drinkLbl,text="Milk",font=("Arial",15,"bold"))
drink1.grid(row=1,column=0,padx=10,pady=10)
drink1qnty=customtkinter.CTkEntry(drinkLbl,font=("Arial",15))
drink1qnty.grid(row=1,column=1)

drink2=customtkinter.CTkLabel(drinkLbl,text="Pepsi",font=("Arial",15,"bold"))
drink2.grid(row=2,column=0,padx=10,pady=10)
drink2qnty=customtkinter.CTkEntry(drinkLbl,font=("Arial",15))
drink2qnty.grid(row=2,column=1)

drink3=customtkinter.CTkLabel(drinkLbl,text="7 Up",font=("Arial",15,"bold"))
drink3.grid(row=3,column=0,padx=10,pady=10)
drink3qnty=customtkinter.CTkEntry(drinkLbl,font=("Arial",15))
drink3qnty.grid(row=3,column=1)

drink4=customtkinter.CTkLabel(drinkLbl,text="Coca Cola",font=("Arial",15,"bold"))
drink4.grid(row=4,column=0,padx=10,pady=10)
drink4qnty=customtkinter.CTkEntry(drinkLbl,font=("Arial",15))
drink4qnty.grid(row=4,column=1)

drink5=customtkinter.CTkLabel(drinkLbl,text="Speed",font=("Arial",15,"bold"))
drink5.grid(row=5,column=0,padx=10,pady=10)
drink5qnty=customtkinter.CTkEntry(drinkLbl,font=("Arial",15))
drink5qnty.grid(row=5,column=1)

drink6=customtkinter.CTkLabel(drinkLbl,text="Sprite",font=("Arial",15,"bold"))
drink6.grid(row=6,column=0,padx=10,pady=10)
drink6qnty=customtkinter.CTkEntry(drinkLbl,font=("Arial",15))
drink6qnty.grid(row=6,column=1)

column_values3 = get_column_values("newproducts3","name")
combobox3 =customtkinter.CTkComboBox(drinkLbl,
                                 values=column_values3,
                                 font=("Arial", 12),width=100)
combobox3.grid(row=7, column=0,padx=10,pady=10)
combobox3qntty=customtkinter.CTkEntry(drinkLbl,font=("Arial",15),width=100)
combobox3qntty.grid(row=7,column=1)
combobox3btn=customtkinter.CTkButton(drinkLbl,text="Add",width=50,command=addCmbItem3)
combobox3btn.grid(row=7,column=2)

combo_dict3 = {}
comblistPrice3 = []
comblistDiscPrice3 = []



# Customer Details fram
customer_dtls_lvl=customtkinter.CTkFrame(customer_dts_Bill)
customer_dtls_lvl.grid(row=0,column=0,ipady=10,ipadx=10,padx=10,pady=10)


# Customer Details:
nameLbl=customtkinter.CTkLabel(customer_dtls_lvl,text="Customer Details",font=("Arial",20,"bold"))
nameLbl.grid(row=0,column=0,columnspan=2,padx=10,pady=5,sticky='ew')

nameLbl=customtkinter.CTkLabel(customer_dtls_lvl,text="Name",font=("Arial",15,"bold"))
nameLbl.grid(row=1,column=0,padx=10,pady=10)

nameEntery=customtkinter.CTkEntry(customer_dtls_lvl,font=("Arial",15))
nameEntery.grid(row=1,column=1)

phonNoLbl=customtkinter.CTkLabel(customer_dtls_lvl,text='Phone',font=("Arial",15,"bold"))
phonNoLbl.grid(row=2,column=0,padx=10,pady=10)

phonEntery=customtkinter.CTkEntry(customer_dtls_lvl,font=("Arial",15))
phonEntery.grid(row=2,column=1)

emailNoLbl=customtkinter.CTkLabel(customer_dtls_lvl,text='Email',font=("Arial",15,"bold"))
emailNoLbl.grid(row=3,column=0,padx=10,pady=10)
emailEntery=customtkinter.CTkEntry(customer_dtls_lvl,font=("Arial",15))
emailEntery.grid(row=3,column=1)



billNoEntery=customtkinter.CTkEntry(customer_dtls_lvl,placeholder_text='Find Bill',font=("Arial",15))
billNoEntery.grid(row=4,column=0,padx=10,pady=10)
billSearch=customtkinter.CTkButton(customer_dtls_lvl,text='Search',font=("Arial",12),command=search_bill)
billSearch.grid(row=4,column=1)

# BILL Frame
billfram=customtkinter.CTkFrame(customer_dts_Bill)
billfram.grid(row=1,column=0,ipadx=10,padx=10)

billLbl=customtkinter.CTkLabel(billfram,text='Bill Area',font=('times new roman',15,'bold'))
billLbl.pack()

bilArea=customtkinter.CTkTextbox(billfram,font=('times new roman',10),fg_color='white',width=350,height=200)
bilArea.pack(padx=20, pady=10,ipadx=10,ipady=10,fill='both',expand=True)

# footer bill menue
footerMenue=customtkinter.CTkFrame(bigFram)
footerMenue.grid(row=2,column=1,columnspan=2,sticky='ew')

# calculatebill
billMenue=customtkinter.CTkFrame(footerMenue,)
billMenue.grid(row=0,column=0,ipadx=10,padx=10,sticky='ew')

# Stasionary price:
stasionaryprice=customtkinter.CTkLabel(billMenue,text="Stasionary Price",font=("Arial",15,"bold"))
stasionaryprice.grid(row=0,column=0,padx=10,pady=10)
stasionarypriceentry=customtkinter.CTkEntry(billMenue,font=("Arial",15))
stasionarypriceentry.grid(row=0,column=1)

#Stasionary tax
stasionaryTax=customtkinter.CTkLabel(billMenue,text="Stasionary Tax",font=("Arial",15,"bold"))
stasionaryTax.grid(row=0,column=2,padx=10,pady=10)
stasionaryTaxentry=customtkinter.CTkEntry(billMenue,font=("Arial",15))
stasionaryTaxentry.grid(row=0,column=3)

# grocery price:
groceryprice=customtkinter.CTkLabel(billMenue,text="Grocery Price",font=("Arial",15,"bold"))
groceryprice.grid(row=1,column=0,padx=10,pady=10)
grocerypriceentry=customtkinter.CTkEntry(billMenue,font=("Arial",15))
grocerypriceentry.grid(row=1,column=1)

#grocery tax
groceryTax=customtkinter.CTkLabel(billMenue,text="Grocery Tax",font=("Arial",15,"bold"))
groceryTax.grid(row=1,column=2,padx=10,pady=10)
groceryTaxentry=customtkinter.CTkEntry(billMenue,font=("Arial",15))
groceryTaxentry.grid(row=1,column=3)

# Drinks price:
drinkprice=customtkinter.CTkLabel(billMenue,text="Drinks Price",font=("Arial",15,"bold"))
drinkprice.grid(row=2,column=0,padx=10,pady=10)
drinkpriceentry=customtkinter.CTkEntry(billMenue,font=("Arial",15))
drinkpriceentry.grid(row=2,column=1)


#Drinks tax
drinkTax=customtkinter.CTkLabel(billMenue,text="Drinks Tax",font=("Arial",15,"bold"))
drinkTax.grid(row=2,column=2,padx=10,pady=10)
drinkTaxentry=customtkinter.CTkEntry(billMenue,font=("Arial",15))
drinkTaxentry.grid(row=2,column=3)


# total Price with tax
total_price=customtkinter.CTkLabel(billMenue,text="Total Price",font=("Arial",15,"bold"))
total_price.grid(row=3,column=0,padx=10,pady=5)
total_priceentry=customtkinter.CTkEntry(billMenue,font=("Arial",15))
total_priceentry.grid(row=3,column=1,)
total_disc=customtkinter.CTkLabel(billMenue,text="Total Discount",font=("Arial",15,"bold"))
total_disc.grid(row=3,column=2,padx=10,pady=5)
disc_entry=customtkinter.CTkEntry(billMenue,font=("Arial",15))
disc_entry.grid(row=3,column=3)

# bill operations
billbotom=customtkinter.CTkFrame(footerMenue)
billbotom.grid(row=0,column=1,ipadx=10,padx=10,sticky='ew')
totalBtn=customtkinter.CTkButton(billbotom,text='Total',font=("Arial",15,"bold"),height=50,command=total)
totalBtn.grid(row=0,column=0,padx=10,pady=10)
BillBtn=customtkinter.CTkButton(billbotom,text='Bill',font=("Arial",15,"bold"),height=50,command=bill_area)
BillBtn.grid(row=0,column=1,padx=10,pady=10)
PrintBtn=customtkinter.CTkButton(billbotom,text='Print',font=("Arial",15,"bold"),height=50,command=print_bill)
PrintBtn.grid(row=0,column=2,padx=10,pady=10)
clearBtn=customtkinter.CTkButton(billbotom,text='Clear',font=("Arial",15,"bold"),height=50,command=clear)
clearBtn.grid(row=0,column=3,padx=10,pady=10)
ExitBtn=customtkinter.CTkButton(billbotom,text='Exit',font=("Arial",15,"bold"),height=50,command=exit)
ExitBtn.grid(row=0,column=4,padx=10,pady=10)

window.mainloop()