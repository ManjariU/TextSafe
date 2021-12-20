# Import the required Libraries
import os
from tkinter import *
from tkinter.filedialog import askopenfile
from cryptography.fernet import Fernet
from pydrive.auth import GoogleAuth 
from pydrive.drive import GoogleDrive

# Create an instance of tkinter frame
win = Tk()
win.title("TextSafe")
content = None
file_name = None
strvar = StringVar(win, "")

# Set the geometry of tkinter frame
win.geometry("700x350")

def open_file():
    global file_name
    global content
    file = askopenfile(mode='r', filetypes=[('text Files', '*.txt'),('encrypted ','*.enc')])
    if file:
        file_name = file.name.split('/')[-1]
        content = str(file.read())
    file.close()
    os.remove(file.name)

def upload_encry(f):
    global file_name
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    file1 = drive.CreateFile({'title':file_name.split(".")[0]+".enc"})
    file1.SetContentFile(f)
    file1.Upload()

def encryptor():
    global content
    global file_name
    key = Fernet.generate_key()
    
    with open('keys.txt','ab') as filekey:
        filekey.write(bytes((file_name.split(".")[0]+" : "),'utf-8'))
        filekey.write(key)
        filekey.write(bytes("\n",'utf-8'))
    original = bytes(content, 'utf-8')
    fernet = Fernet(key)
    encrypted = fernet.encrypt(original)

    # writing encrypted data
    with open(file_name.split(".")[0]+".enc",'wb') as enc_file:
        enc_file.write(encrypted)
    upload_encry(file_name.split(".")[0]+".enc")

def decryptor():
    global content
    global file_name
    key = strvar.get()
    fernet = Fernet(key)
    encrypted =  bytes(content,"utf-8")
    decrypted = fernet.decrypt(encrypted)

    with open(file_name.split(".")[0]+".txt",'wb') as dec_file:
        dec_file.write(decrypted)

# Create a Buttons and Labels

# canvas = Canvas(win)      
# canvas.pack()      
# img = PhotoImage(file="drivelogo.png")      
# canvas.create_image(20,20, anchor=E, image=img)      

Label(win, text="Click below to browse files",fg="black",font = ("Times",12)).pack()
Button(win, text= "Browse",width = 20,command=open_file).pack(pady=20)
Button(win, text = "Encrypt",bg='green',width = 20, command= encryptor).pack(pady=20)
Label(win, text="Enter the key to decrypt",fg="black",font = ("Times",12)).pack()
T = Entry(win, width=20, textvariable=strvar)
T.pack(pady = 20)
Button(win, text = "Decrypt",bg='red',width = 20,command= decryptor).pack(pady=20)
win.mainloop()