import os
import paramiko
import shutil

def download_and_zip_jobs_folder(host, port, username, password, remote_path, local_path, zip_filename):
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    local_temp_path = os.path.join(local_path, 'temp')
    os.makedirs(local_temp_path, exist_ok=True)

    # Download jobs folder recursively
    download_recursive(sftp, remote_path, local_temp_path)

    # Zip the downloaded folder
    shutil.make_archive(os.path.join(local_path, zip_filename), 'zip', local_temp_path)

    print(f"ZIP file '{zip_filename}.zip' created successfully.")

    # Cleanup: Remove the temporary folder
    shutil.rmtree(local_temp_path)

    sftp.close()
    transport.close()

def download_recursive(sftp, remote_path, local_path):
    for item in sftp.listdir_attr(remote_path):
        remote_item_path = f"{remote_path}/{item.filename}"
        local_item_path = os.path.join(local_path, item.filename)

        if stat.S_ISDIR(item.st_mode):
            os.makedirs(local_item_path, exist_ok=True)
            download_recursive(sftp, remote_item_path, local_item_path)
        else:
            sftp.get(remote_item_path, local_item_path)

# Replace these values with your actual credentials and paths
remote_ip = 'XX.XX.XX.XX'  # Replace with your VM's IP address
remote_port = 22
remote_path = "/home/jenkins/CORELOAD-INBLRJENKINS01/jenkins_home/"
local_path = r"C:\Users\YourUsername\Documents"
zip_filename = 'jenkins_home_archive'

username = 'your_ssh_username'
password = 'your_ssh_password'

download_and_zip_jobs_folder(remote_ip, remote_port, username, password, remote_path, local_path, zip_filename)
