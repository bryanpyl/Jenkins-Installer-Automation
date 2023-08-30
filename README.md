# Jenkins-Installer-Automation
Demonstration of NSIS script compilation containing Python executables into customized Windows Installers using Jenkins automation mechanisms

**Prerequisite:**
1. Jenkins (open-source automation server)
2. Excel file containing user credentials
2. MySQL database (or relevant databases)
3. Valid email credentials 


**Automation Steps (Description):**
1. Create an Excel file containing user credentials (Username, Password, and Email)
2. Generate a random password for each user in the Excel file that initially does not possess one.
3. Upload or synchronize the Excel file data into a MySQL database
4. Generate customized Python executables according to the credentials from the database
5. Create and modify a custom NSIS installer script for each user containing respective Python executables
6. Compile all NSIS scripts into customized Windows installer executables 
7. Compress all Windows installers into individual zip files and email them to respective users as attachments
