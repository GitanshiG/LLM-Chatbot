import smtplib
from config import SENDER_EMAIL,PASSWORD
from email.message import EmailMessage

def send_email(reciever_mail, subject, content):
    """This function is used to send email.
    
        Input:
            reciever_mail: The email address of reciever
            subject: The subject of email
            content: The content of email          
    
    """
    # Define email details
    sender = SENDER_EMAIL
    password = PASSWORD  # Use an App Password, not your main password
    recipient = reciever_mail
    subject = subject
    body = content

    # Create the message object
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    msg.set_content(body)

    # Connect and send
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)   


    return "Mail sent successfully."

send_email("jayantdixit2406@gmail.com", "Apology for not responding"," I beg to say i couldn't hear your voice yesterday on the meet.")