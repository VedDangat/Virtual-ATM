import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


import time

def sendEmail(to,subject,body):
    
 
    
    
    #The mail addresses and password
    sender_address ="innovatusproject.testing@gmail.com"
    sender_pass = "ixvo xoty qgds adta"
    print("")
  
    
    
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = to
    message['Subject'] = subject   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(body, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, to, text)
    session.quit()
   # time.sleep(10)
    print('Mail Sent')
    value =1
    return value
    
  
 