import smtplib
from os import path

def create_file(destination):
    if not path.isfile(destination):
        with open(destination, 'w') as file:
            file.write('Hello, World!')

def send_email(sender_email, sender_password, recipient_email, subject, body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    message = 'Subject: {}\n\n{}'.format(subject, body)
    server.sendmail(sender_email, recipient_email, message)
    server.quit()

# Necessary inputs
destination = input("Enter the destination file path: ")
sender_email = input("Enter your email: ")
sender_password = input("Enter your email password: ")
recipient_email = input("Enter the recipient's email: ")
subject = input("Enter the email subject: ")
body = input("Enter the email body: ")

# Intialize the functions
create_file(destination)
send_email(sender_email, sender_password, recipient_email, subject, body)
