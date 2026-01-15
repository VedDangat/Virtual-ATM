import tkinter as tk
from tkinter import *
from threading import Thread
import TransactionData
from tkinter import messagebox




def action_one(event=None):
  
    print("Action1 Called")
    userotp=textBox1.get()
    print("userotp ",userotp)
    print("Emailed OTP ",TransactionData.otp)
    if(TransactionData.otp==userotp):
        messagebox.showinfo("Success Message", "OTP Matched")
        root.withdraw()
        import TransactionGUIForm
        startTranscationguithread = Thread(target = TransactionGUIForm.transcationWindowGUI, args = (12,))
        startTranscationguithread.start()
        TransactionGUIForm.root.mainloop()
        textBox1.insert(0, "")
    else:
        textBox1.insert(0, "")
        messagebox.showinfo("Error Message", "OTP Mismatched Please Try Again" )
       
       
    

root = tk.Tk() 
root.title("OTP AuthenticationPanel")
canvas = tk.Canvas(root, width=1500, height=1000)
canvas.pack()
canvas.create_rectangle(1000, 200, 400, 400, fill='#fb0')   
textBox1 = tk.Entry(root, width = 25)
textBox1.place(x = 625,y = 250,height=35)
def OTPGUIFORM(arg):
    global root    
            
    
   
    global textBox1
     
    
    textBox1 = tk.Entry(root, width = 25)
    textBox1.place(x = 625,y = 250,height=35)
    
    textBox1.insert(0, "")
    
    button1=tk.Button(root, text="SUBMIT",height=2,width=20,command=action_one)
    button1.place(x=625, y=300)
    text_1 = Label(text="SHRI CHATRAPATI SHIVAJI CO-OPERATIVE BANK, AHMED NAGAR", bg='white', font=("Ariel", 20, "italic"), fg='black')
    text_1.place(x=300, y=60)
    text_1_1 = Label(text="ENTER OTP RECEIVED ON YOUR REGISTERED EMAIL ID", bg='white', font=("Ariel", 10, "italic"), fg='black')
    text_1_1.place(x=490, y=210)
    
   # root.mainloop()

if __name__ == "__main__":
    starterguithread = Thread(target = OTPGUIFORM, args = (12,))
    starterguithread.start()
    root.mainloop()
     