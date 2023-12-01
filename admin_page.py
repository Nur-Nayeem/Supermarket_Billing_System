import os
from tkinter import *
from tkinter import messagebox
import customtkinter
from PIL import Image, ImageTk

def back():
    frnt.withdraw()
    os.system("python front.py")
    frnt.destroy()
    os._exit(0)


def empl():
    frnt.withdraw()
    os.system("python Add_Employee.py")
    frnt.destroy()
    os._exit(0)

def prod():
    frnt.withdraw()
    os.system("python add_product.py")
    frnt.destroy()
    os._exit(0)
def customers():
    frnt.withdraw()
    os.system("python customers.py")
    frnt.destroy()
    os._exit(0)


customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

frnt=Tk()
frnt.title("Admin Page")
frnt.geometry("1000x600+250+100")
frnt.resizable(False,False)

# Add image file 
bg = PhotoImage(file = "bgg.png")
# Show image using label 
label = Label( frnt, image = bg,height=600,width=1000) 
label.place(x = 0, y = 0) 

backBtn=customtkinter.CTkButton(frnt,text="BACK",cursor="hand2",command=back)
backBtn.place(x=10,y=10)

label1 = customtkinter.CTkLabel(frnt,text="All About",bg_color="#e3d2b3",font=("times new roman",30,"bold"))
label1.pack(side=TOP,pady=100)

img1 = customtkinter.CTkImage(Image.open("products.png"),size=(131,124))
button1 = customtkinter.CTkButton(frnt,text="",image=img1,corner_radius=5,cursor="hand2",fg_color="#e3d2b3",bg_color="#e3d2b3",hover_color='#decaa4',command=prod)
button1.place(x=250, y=200)
label11 = customtkinter.CTkLabel(frnt,text="Products",bg_color="#e3d2b3",font=("times new roman",20,"bold"))
label11.place(x=284, y=340)


img2 = customtkinter.CTkImage(Image.open("emp.png"),size=(131,124))
button2 = customtkinter.CTkButton(frnt,text="",image=img2,corner_radius=5,cursor="hand2",fg_color="#e3d2b3",bg_color="#e3d2b3",hover_color='#decaa4',command=empl)
button2.place(x=450, y=200)
label22 = customtkinter.CTkLabel(frnt,text="Employees",bg_color="#e3d2b3",font=("times new roman",20,"bold"))
label22.place(x=480, y=340)

img3 = customtkinter.CTkImage(Image.open("cstomers.png"),size=(131,124))
button3 = customtkinter.CTkButton(frnt,text="",image=img3,corner_radius=5,cursor="hand2",fg_color="#e3d2b3",bg_color="#e3d2b3",hover_color='#decaa4',command=customers)
button3.place(x=650, y=200)
label22 = customtkinter.CTkLabel(frnt,text="Customers",bg_color="#e3d2b3",font=("times new roman",20,"bold"))
label22.place(x=680, y=340)



frnt.mainloop()