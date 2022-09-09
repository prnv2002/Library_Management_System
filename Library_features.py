import smtplib
import datetime
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import matplotlib.pyplot as plt
import numpy as np

def issue_mail(Fname ,Lname, Bname, Duedate, from_id ,to_id, password):
    message = f"""Thanks {Fname} {Lname},<br>
        For issuing book Named <b>'{Bname}'</b> from our library.<br>
        The Due date for returning the book is <b>{Duedate}</b><br>
        <i>\" WE DO BELIEVE SOMETHING GREAT WILL HAPPEN ,WHEN YOU READ A GOOD BOOK!!!!\" </i>"""
    HTML_BODY = MIMEText(message, 'html')

    msg = MIMEMultipart('alternative')
    msg['subject'] = "Book Issued"
    msg['From'] = from_id
    msg['To'] = to_id
    msg.attach(HTML_BODY)


    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(from_id,password)
    server.sendmail(from_id,to_id,msg.as_string())
    server.quit()

def remainder_mail(Fname ,Lname, Bname, Duedate, from_id ,to_id, password):
    message = f"""Dear {Fname} {Lname},<br>
        Thanks for issuing book Named <b>'{Bname}'</b> from our library.<br>
        The Due date for returning the book is Tomorrow i.e.<b>{Duedate}</b><br>
        Kindly return the book by tomorrow or else Rs.5/day will be fined after the due date."""
    HTML_BODY = MIMEText(message, 'html')

    msg = MIMEMultipart('alternative')
    msg['subject'] = "Remainder For Returning Book"
    msg['From'] = from_id
    msg['To'] = to_id
    msg.attach(HTML_BODY)


    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(from_id,password)
    server.sendmail(from_id,to_id,msg.as_string())
    server.quit()



def make_graph(x_terms,y_terms):
    xpos= np.arange(len(x_terms))
    plt.xlabel("Genre")
    plt.ylabel("Times Issued")
    plt.xticks(xpos,x_terms)
    plt.bar(xpos,y_terms,label="Issues")
    plt.legend()    
    plt.show()