import os
import pandas as pd
import mysql.connector
from mysql.connector import errorcode

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",  # MySQL username
    "password": "",  # MySQL password (leave empty if no password)
    "database": "Jenkins",
}

# Replace the file path with your exact Excel file path
excel_file_path = "C:\\Users\\user\\OneDrive\\Desktop\\SAINS\\Jenkins-Installer-Automation\\UserList.xlsx"

def synchronize_data():
    try:
        # Connect to the MySQL database
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Read the Excel file
        excel_data = pd.read_excel(excel_file_path)

        # Retrieve existing usernames from the user table
        cursor.execute("SELECT Username FROM user")
        existing_usernames = [row[0] for row in cursor.fetchall()]

        # Compare and synchronize data
        for index, row in excel_data.iterrows():
            username = row["Username"]
            password = row["Password"]
            email = row["Email"]

            if username in existing_usernames:
                # Check if data needs to be updated
                select_query = "SELECT Password, Email FROM user WHERE Username = %s"
                cursor.execute(select_query, (username,))
                db_password, db_email = cursor.fetchone()

                if password != db_password or email != db_email:
                    # Update record
                    update_query = "UPDATE user SET Password = %s, Email = %s WHERE Username = %s"
                    cursor.execute(update_query, (password, email, username))
            else:
                # Insert new record
                insert_query = "INSERT INTO user (Username, Password, Email) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (username, password, email))

            if username in existing_usernames:
                existing_usernames.remove(username)  # Mark this username as found

            cnx.commit()

        # Delete records that are no longer present in the Excel file
        for username_to_delete in existing_usernames:
            delete_query = "DELETE FROM user WHERE Username = %s"
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
