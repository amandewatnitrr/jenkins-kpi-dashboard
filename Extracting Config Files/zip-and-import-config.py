import paramiko
import os

def zip_and_download_jobs_folder(host, port, username, password, remote_path, local_path):
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Remote command to zip the jobs folder
    zip_command = f"cd {remote_path} && zip -r - jobs > jobs.zip"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=port, username=username, password=password)
    ssh.exec_command(zip_command)
    ssh.close()

    # Download the zipped file
    remote_zip_path = os.path.join(remote_path, 'jobs.zip')
    local_zip_path = os.path.join(local_path, 'jobs.zip')
    sftp.get(remote_zip_path, local_zip_path)

    print(f"ZIP file downloaded to: {local_zip_path}")

    # Cleanup: Remove the remote zipped file
    sftp.remove(remote_zip_path)

    sftp.close()
    transport.close()

# Replace these values with your actual credentials and paths
remote_ip = 'XX.XX.XX.XX'
remote_port = 22
remote_path = "/home/jenkins/CORELOAD-INBLRJENKINS01/jenkins_home"
local_path = r"C:\Users\YourUsername\Documents"

username = 'your_username'
password = 'your_password'

zip_and_download_jobs_folder(remote_ip, remote_port, username, password, remote_path, local_path)
