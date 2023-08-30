import sys
import os
import shutil
import re

def create_nsis_script_for_file(file_path, output_folder, nsis_script_path):
    with open(nsis_script_path, 'r') as f:
        script_content = f.read()

    new_file_name = os.path.basename(file_path)
    installer_name = f"{os.path.splitext(new_file_name)[0]}_installer"

    modified_script_name = f"modified_{new_file_name}_{os.path.basename(nsis_script_path)}"

    # Replace File path (@@FILE_PATH@@)
    modified_script_content = script_content.replace("@@FILE_PATH@@", file_path.replace("\\", "\\"))

    # Replace Installer name (@@INSTALLER_NAME@@)
    modified_script_content = modified_script_content.replace("@@INSTALLER_NAME@@", installer_name)

    # Replace ExecToStack path
    old_exec_pattern = r'nsExec::ExecToStack \'cmd.exe /C "echo \$Creds\| "(.*?)" \$Username \$Password"'
    # Search 'old_exec_pattern' within the 'modified_script_content'
    old_exec_match = re.search(old_exec_pattern, modified_script_content)

    if old_exec_match:
        # Extract captured path from regular expression match
        old_exec_path = old_exec_match.group(1)
        # Get last part of the old path (the filename) by splitting the path
        new_exec_path = old_exec_path.replace(old_exec_path.split("\\")[-1], new_file_name)
        # Create new path by replacing old_exec_path
        modified_script_content = modified_script_content.replace(old_exec_path, new_exec_path)

    modified_script_path = os.path.join(output_folder, modified_script_name)

    # Write the modified script content to a new file in the output folder
    with open(modified_script_path, 'w') as f:
        f.write(modified_script_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python replace_file_path.py <input_folder_path> <output_folder_name>")
    else:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2]

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Replace NSIS script file path with exact script path
        nsis_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "C:\\Users\\user\\OneDrive\\Desktop\\SAINS\\Jenkins-Installer-Automation\\installer.nsi")

        for root, _, files in os.walk(input_folder):
            for file in files:
                file_path = os.path.join(root, file)
                create_nsis_script_for_file(file_path, output_folder, nsis_script_path)

        print("NSIS scripts created successfully.")





# python replace_file_path.py "C:\\Users\\user\\OneDrive\\Desktop\\SAINS\\Week_6\\21.8.2023\\user_exe_files" output 