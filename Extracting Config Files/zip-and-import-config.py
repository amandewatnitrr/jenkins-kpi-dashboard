import os
import paramiko
import shutil

def zip_and_move_jobs_folder(host, port, username, password, remote_path, tmp_path, local_path, zip_filename):
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    
    # SSHClient to execute commands
    ssh = paramiko.SSHClient()
    ssh._transport = transport
    
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Step 1: Zip the "jobs" folder on the VM
    zip_filepath = os.path.join(remote_path, f"{zip_filename}.zip")
    zip_command = f"cd {remote_path} && zip -r {zip_filename}.zip jobs"
    ssh.exec_command(zip_command)

    # Step 2: Move the ZIP file to /tmp on the VM
    move_command = f"mv {zip_filepath} {tmp_path}"
    ssh.exec_command(move_command)

    # Step 3: Download the ZIP file to the local computer
    local_zip_filepath = os.path.join(local_path, f"{zip_filename}.zip")
    sftp.get(os.path.join(tmp_path, f"{zip_filename}.zip"), local_zip_filepath)

    # Step 4: Cleanup: Remove the ZIP file from /tmp on the VM
    remove_command = f"rm {os.path.join(tmp_path, f'{zip_filename}.zip')}"
    ssh.exec_command(remove_command)

    sftp.close()
    transport.close()

    print(f"ZIP file '{local_zip_filepath}' created and downloaded successfully.")

# Replace these values with your actual credentials and paths
remote_ip = 'XX.XX.XX.XX'
remote_port = 22
username = 'your_username'
password = 'your_password'
remote_path = "/home/jenkins/CORELOAD-INBLRJENKINS01/jenkins_home/"
tmp_path = "/tmp"
local_path = r"C:\Users\YourUsername\Downloads"
zip_filename = 'jobs_archive'

zip_and_move_jobs_folder(remote_ip, remote_port, username, password, remote_path, tmp_path, local_path, zip_filename)
