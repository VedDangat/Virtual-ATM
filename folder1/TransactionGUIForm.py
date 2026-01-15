import tkinter as tk
from tkinter import *
from threading import Thread
from tkinter import messagebox
import TransactionData
from datetime import datetime
import mysql.connector
import EMAILSender


def action_one(event=None):
   
  
    print("Action1 Called")
    balanceamount=TransactionData.accountbalance
    print("balanceamount ",balanceamount)
    baltext="Rs "+balanceamount+".00"
    messagebox.showinfo("Account Balance", baltext)
    
   
   
    

def action_two(event=None):
    print("Action2 Called")
    amountstr=textBox3.get()
    print("amountstr ",amountstr)
    balanceamount=TransactionData.accountbalance
    print("balanceamount ",balanceamount)
    entamt=int(amountstr)
    currbalance=int(balanceamount)
    if(entamt>currbalance):
        messagebox.showinfo("Alert Message", "Sorry You Dont have Sufficeint Balance")
    else:
        rem=entamt%100
        if(rem==0):
            
            rembal=currbalance-entamt
            print("Remaining balance is ",rembal)
            
            strrembal=str(rembal)
            accountnum=TransactionData.accountno
            mydb = mysql.connector.connect( host="localhost", user="root",  passwd="root",  database="virtualatm")
            mycursor = mydb.cursor()
            sql="UPDATE account_info SET initial_amt='"+strrembal+"' where account_no='"+accountnum+"' ";
            mycursor.execute(sql)
            mydb.commit()
    
            print(mycursor.rowcount, "record Updated.")
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            mailtext="Dear Customer \n Your Account number "+TransactionData.accountno+"  has been Debited for Rs "+amountstr+" on "+dt_string+".\n And the current Availaible Balance is Rs "+strrembal+" \n Thank your Using our Services from SCSCOP Bank"
            to=TransactionData.emailid
            val=EMAILSender.sendEmail(to,"Regarding ATM Debit",mailtext)
            val=1
            if(val==1):
                
                textmsg="Please collect your cash of "+amountstr+" \n Thank you for using our Services"
                messagebox.showinfo("Withdraw Message",textmsg)
                print("mailtext : ",mailtext)
                root.withdraw()
        else:
            
            messagebox.showinfo("Alert Message",'Please Enter Amount in Multiple of 100s')

        
root = tk.Tk()
root.title("TRANSCATION FORM")
canvas = tk.Canvas(root, width=1500, height=1000)
canvas.pack()
canvas.create_rectangle(1000, 200, 400, 400, fill='#fb0')
canvas.create_rectangle(1000, 450, 400, 750, fill='#63775b')

textBox3 = tk.Entry(root, width = 23)
textBox3.place(x = 560,y = 530,height=35)
def transcationWindowGUI(arg):
    
    global root    
            
    
   
    global textBox3
    
    button1=tk.Button(root, text="CLICK HERE TO CHECK BALANCE",height=2,width=30,command=action_one)
    button1.place(x=560, y=280)
    text_1 = Label(text="CHECK YOUR BALANCE", bg='white', font=("Ariel", 10, "italic"), fg='black')
    text_1.place(x=560, y=160)
    
    
    
    textBox3.insert(0, "")
    
    button2=tk.Button(root, text="WITHDRAW",height=1,width=23,command=action_two)
    button2.place(x=560, y=600)
    text_2 = Label(text="WITHDRAW AMOUNT", bg='white', font=("Ariel", 10, "italic"), fg='black')
    text_2.place(x=560, y=410)
    
    text_2_1 = Label(text="ENTER AMOUNT HERE", bg='white', font=("Ariel", 10, "italic"), fg='black')
    text_2_1.place(x=560, y=470)
   # root.mainloop()
if __name__ == "__main__":
    startTranscationguthread = Thread(target = transcationWindowGUI, args = (12,))
    startTranscationguthread.start()
    root.mainloop()