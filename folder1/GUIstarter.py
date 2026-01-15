import OTPGUIFORM
from threading import Thread
import random
import mysql.connector #pip install mysql-connector
import EMAILSender
import TransactionData

def startGUI(username):
    ran=random.randint(10001, 99999)
    otpstr=str(ran)
    print("OTP Is ",otpstr)
    conn = mysql.connector.connect(user='root', password='root', host='localhost', database='virtualatm')
    cursor = conn.cursor()
    sql = "SELECT account_no,email_id,initial_amt from account_info where customer_name='"+username+"'"
    cursor.execute(sql)
    customer_list=cursor.fetchone()
    conn.close()
    
    print("Account No is: ",customer_list[0])
    print("Email Id is: ",customer_list[1])
    print("Balance is: ",customer_list[2])
    TransactionData.setParameters(customer_list[0], customer_list[2], otpstr,customer_list[1])
        
    to=customer_list[1]
    sub="OTP For Virtual ATM"
    body="Dear Customer \n Your OTP For ATM Transcation is "+otpstr
    print("Body is :", body)
    val=EMAILSender.sendEmail(to,sub,body)
    val=1
    if(val==1):     
        
        guithread1 = Thread(target = OTPGUIFORM.OTPGUIFORM, args = (12,))
        
        guithread1.start()
        OTPGUIFORM.root.mainloop()


#startGUI("Pravin")