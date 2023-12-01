import os
from tkinter import *
from tkinter import messagebox
import customtkinter
from PIL import Image, ImageTk




def emp():
    frnt.withdraw()
    os.system("python emplogin.py")
    frnt.destroy()
    os._exit(0)

def adm():
    frnt.withdraw()
    os.system("python admin_login.py")
    frnt.destroy()
    os._exit(0)


customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

frnt=Tk()
frnt.title("Super Market Billing System")
frnt.geometry("1000x600+200+100")
frnt.resizable(False,False)

# Add image file 
bg = PhotoImage(file = "bgg.png")
# Show image using label 
label = Label( frnt, image = bg,height=600,width=1000) 
label.place(x = 0, y = 0) 

label1 = customtkinter.CTkLabel(frnt,text="Login As",font=("times new roman",30,"bold"),bg_color="#e3d2b3")
label1.pack(side=TOP,pady=100)

img1 = customtkinter.CTkImage(Image.open("adm.png"),size=(131,120))
button1 = customtkinter.CTkButton(frnt,text="",image=img1,corner_radius=5,cursor="hand2",command=adm,fg_color="#e3d2b3",bg_color="#e3d2b3",hover_color='#decaa4')
button1.place(x=340, y=200)
label11 = customtkinter.CTkLabel(frnt,text="Admin",font=("times new roman",20,"bold"),bg_color="#e3d2b3")
label11.place(x=380, y=340)

img2 = customtkinter.CTkImage(Image.open("emp.png"),size=(131,120))
button2 = customtkinter.CTkButton(frnt,text="",image=img2,corner_radius=5,cursor="hand2",command=emp,fg_color="#e3d2b3",bg_color="#e3d2b3",hover_color='#decaa4')
button2.place(x=540, y=200)
label22 = customtkinter.CTkLabel(frnt,text="Employee",font=("times new roman",20,"bold"),bg_color="#e3d2b3")
label22.place(x=570, y=340)





frnt.mainloop()