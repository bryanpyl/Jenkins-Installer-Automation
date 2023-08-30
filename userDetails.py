import os
import subprocess
import mysql.connector
from mysql.connector import errorcode

def generate_user_exe_from_database():
    try:
        # Database configuration
        db_config = {
            "host": "localhost",
            "user": "root",  # MySQL username
            "password": "",  # MySQL password (leave empty if no password)
            "database": "Jenkins",
        }

        # Connect to the MySQL database
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Retrieve user details from the database
        query = "SELECT Username, Password, Email FROM user"
        cursor.execute(query)
        user_data = cursor.fetchall()

        output_dir = os.path.join(os.getcwd(), "user_exe_files")
        os.makedirs(output_dir, exist_ok=True)

        for username, password, email in user_data:
            script_content = f"""
import sys
import time
            
username = "{username}"
password = "{password}"
email = "{email}"

# Define valid credentials (replace these with your actual valid credentials)
VALID_USERNAME = username
VALID_PASSWORD = password

# Compare username and password
def authenticate(username, password):
    if not username or not password:
        print("EMPTY")
    elif username == VALID_USERNAME and password == VALID_PASSWORD:
        print("SUCCESS")
    else:
        print("FAILURE")

# Main function
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("EMPTY")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]
    #delay for 3 seconds
    
    authenticate(username, password)
    time.sleep(3)
    print("FINISH")
"""

            temp_py_file = f"{username}.py"
            with open(temp_py_file, "w") as file:
                file.write(script_content)

            subprocess.run([
                'pyinstaller',
                '--onefile',
                '--distpath',
                output_dir,
                temp_py_file
            ])

            os.remove(temp_py_file)

            print(f"{username}.exe generated with user details.")

        cursor.close()
        cnx.close()

    except mysql.connector.Error as err:
        print("MySQL Error:", err)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_user_exe_from_database()
