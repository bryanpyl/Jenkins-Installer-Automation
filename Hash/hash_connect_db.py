import os
import hashlib
import pandas as pd
import mysql.connector
from mysql.connector import errorcode

# Database configuration
db_config = {
    "host": "localhost",    # Replace with your exact MySQL host
    "user": "root",         # Replace with your exact MySQL username
    "password": "",         # Replace with yourMySQL password (leave empty if no password)
    "database": "Jenkins",  # Replace with your exact MySQL database name
}

# Replace the file path with your exact Excel file path
excel_file_path = "C:\\Users\\user\\OneDrive\\Desktop\\SAINS\\Jenkins-Installer-Automation\\UserList.xlsx"

def hash_password(password):
    # Hash the password using SHA-256
    hash_object = hashlib.sha256(password.encode())
    return hash_object.hexdigest()

def synchronize_data():
    try:
        # Connect to the MySQL database
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Read the Excel file
        excel_data = pd.read_excel(excel_file_path)

        # Retrieve existing usernames from the hash table in Jenkins database
        cursor.execute("SELECT Username FROM hash")
        existing_usernames = [row[0] for row in cursor.fetchall()]

        # Compare and synchronize data
        for index, row in excel_data.iterrows():
            username = row["Username"]
            raw_password = row["Password"]  # Get the raw password from the Excel file
            hashed_password = hash_password(raw_password)  # Hash the password
            email = row["Email"]  # Get the email from the Excel file

            if username in existing_usernames:
                select_query = "SELECT Password, Email FROM hash WHERE Username = %s"
                cursor.execute(select_query, (username,))
                db_hashed_password, db_email = cursor.fetchone()

                if hashed_password != db_hashed_password or email != db_email:
                    update_query = "UPDATE hash SET Password = %s, Email = %s WHERE Username = %s"
                    cursor.execute(update_query, (hashed_password, email, username))
            else:
                insert_query = "INSERT INTO hash (Username, Password, Email) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (username, hashed_password, email))

            if username in existing_usernames:
                existing_usernames.remove(username)

            cnx.commit()

        # Delete records that are no longer present in the Excel file
        for username_to_delete in existing_usernames:
            delete_query = "DELETE FROM hash WHERE Username = %s"
            cursor.execute(delete_query, (username_to_delete,))
            cnx.commit()

        cursor.close()
        cnx.close()

        print("Data synchronized successfully.")

    except mysql.connector.Error as err:
        print("MySQL Error:", err)

if __name__ == "__main__":
    if os.path.exists(excel_file_path):
        synchronize_data()
    else:
        print("Excel file not found.")
