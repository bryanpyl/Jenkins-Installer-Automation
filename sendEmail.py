import os
import smtplib
import pymysql
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Setup port number and server name
smtp_port = 587  # Standard secure SMTP port
smtp_server = "smtp.gmail.com"  # Google SMTP Server

# Set up the email sender
email_from = "user@gmail.com"
# Replace the password with Google App Password for security reasons
# Remember to save the passwords in a safe file or folder
pswd = " "

# Define the email subject
subject = "Jenkins Zip File!!"

# Define the email function
def send_emails(email_list):
    for username, email in email_list:
        # Make the body of the email
        body = f"""
        Testing with sending email with file attached to user {username}
        """

        # Make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = f"{username} <{email}>" 
        msg['Subject'] = subject

        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))

        zip_folder_path = "C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\Jenkins_Installer_Automation\\zip\\"


        # Define the zip file to attach based on the username
        zip_filename = f"{zip_folder_path}{username}_installer.zip"
        
        # Open the zip file in python as a binary
        attachment = open(zip_filename, 'rb')

        # Encode as base 64
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload(attachment.read())
        encoders.encode_base64(attachment_package)
        
        # Set the attachment's display name to the extracted filename
        attachment_name = f"{username}.zip"
        attachment_package.add_header('Content-Disposition', f"attachment; filename= {attachment_name}")
        msg.attach(attachment_package)

        # Cast as string
        text = msg.as_string()

        # Connect with the server
        print("Connecting to the server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Successfully connected to the server")
        print()

        # Send emails to "person" as the list is iterated
        print(f"Sending email to: {email}...")
        TIE_server.sendmail(email_from, email, text)
        print(f"Email sent to: {email}")
        print()

        # Close the connection
        TIE_server.quit()

# Establish a connection to the database
db_connection = pymysql.connect(
    host="localhost",  # Your database host
    user="root",  # Your database username
    password="",  # Your database password
    database="Jenkins"  # Your database name
)

# Create a cursor object
cursor = db_connection.cursor()

# Query to fetch usernames and corresponding email addresses from the 'user_email' table
query = "SELECT username, email FROM user_email"
cursor.execute(query)
result_set = cursor.fetchall()

# Close the cursor and database connection
cursor.close()
db_connection.close()

# Prepare the email list from the query results
email_list = result_set

# Run the function with the retrieved email list
send_emails(email_list)
