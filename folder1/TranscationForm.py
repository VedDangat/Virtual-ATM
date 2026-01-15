import tkinter as tk
from tkinter import *




def action_one(event=None):
    board = pyfirmata.Arduino('COM15')
    it = pyfirmata.util.Iterator(board)
    it.start()
    print("Action1 Called")
    v1=textBox1.get()
    v2=textBox2.get()
    if(len(v1)>0 and len(v2)>0):
        x=int(v1)
        y=int(v2)
        if((x==1 or x==0) and ( y==1 or y==0)):
            print(" Numbers are correct")
            if( x==1 and y==1):
                text="The value of X and Y are One and we are applying AND gate, So both the Lights are on for 10 Seconds"
                playvoice(text)
            elif( x==1 and y==0):
                 text="The value of X is one and Y is Zero and we are applying AND gate, So One Light will be  on for 10 Seconds"
                 playvoice(text) 
            elif( x==0 and y==1):
                 text="The value of X is Zero and Y is One and we are applying AND gate, So One Light will be  on for 10 Seconds"
                 playvoice(text)       
            elif( x==0 and y==0):
                 text="The value of X is Zero and Y is Zero and we are applying AND gate, So One Light will be  on for 10 Seconds"
                 playvoice(text)
            if x & y: # applying AND GATE
                board.digital[13].write(1)
                board.digital[2].write(1)
                time.sleep(10)
                board.digital[13].write(0)
                board.digital[2].write(0)
                it.join()
            else:
                board.digital[13].write(1)
                board.digital[2].write(0)
                time.sleep(10)
                board.digital[13].write(0)
                board.digital[2].write(0)
                it.join()     
        else:
            messagebox.showinfo("Error Message", "Values should be 1 or 0")
            
        
        
    else:
        messagebox.showinfo("Error Message", " Please Enter the Integer Values")
    
    
    
        
root = tk.Tk()
root.title("OTP AuthenticationPanel")
canvas = tk.Canvas(root, width=1500, height=1000)
canvas.pack()
canvas.create_rectangle(100, 100, 400, 400, fill='#fb0')
canvas.create_rectangle(100, 450, 400, 750, fill='#63775b')

 

textBox1 = tk.Entry(root, width = 10)
textBox1.place(x = 250,y = 120,height=35)
textBox2 = tk.Entry(root, width = 10)
textBox2.place(x = 250,y = 200,height=35)
textBox1.insert(0, "")
textBox2.insert(0, "")
button1=tk.Button(root, text="SUBMIT",height=1,width=10,command=action_one)
button1.place(x=250, y=280)
text_1 = Label(text="AND GATE", bg='white', font=("Ariel", 10, "italic"), fg='black')
text_1.place(x=200, y=60)
text_1_1 = Label(text="VALUE 1", bg='white', font=("Ariel", 10, "italic"), fg='black')
text_1_1.place(x=120, y=120)

root.mainloop()